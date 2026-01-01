"""
Reusable GitHub CLI operations for working with pull requests.

This module provides wrapper functions around the GitHub CLI (gh) for common
PR operations like fetching data, approving, and enabling auto-merge.
"""

import json
import subprocess
from typing import List, Optional

from hexagon.support.output.printer import log

GITHUB_ORGANIZATION = "lt-mayonesa"


def execute_graphql_query(query: str, variables: dict) -> Optional[dict]:
    """
    Execute a GraphQL query using gh CLI.

    Args:
        query: GraphQL query string
        variables: Dictionary of variables for the query

    Returns:
        Parsed JSON response or None if the query failed
    """
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]

    # Add variables as -F flags
    for key, value in variables.items():
        cmd.extend(["-F", f"{key}={value}"])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        log.error(f"GraphQL query failed: {result.stderr}")
        return None

    return json.loads(result.stdout)


def get_pr_files(repo: str, pr_number: int) -> Optional[List[dict]]:
    """
    Get the list of files changed in a PR with their stats.

    Args:
        repo: Repository name (without organization)
        pr_number: PR number

    Returns:
        List of file dictionaries with 'path', 'additions', 'deletions' keys,
        or None if the request failed
    """
    result = subprocess.run(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "-R",
            f"{GITHUB_ORGANIZATION}/{repo}",
            "--json",
            "files",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error(f"Failed to get PR files: {result.stderr}")
        return None

    pr_data = json.loads(result.stdout)
    return pr_data.get("files", [])


def get_pr_diff(repo: str, pr_number: int) -> Optional[str]:
    """
    Get the unified diff for a PR.

    Args:
        repo: Repository name (without organization)
        pr_number: PR number

    Returns:
        Unified diff string or None if the request failed
    """
    result = subprocess.run(
        ["gh", "pr", "diff", str(pr_number), "-R", f"{GITHUB_ORGANIZATION}/{repo}"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error(f"Failed to get diff: {result.stderr}")
        return None

    return result.stdout


def get_pr_node_id(repo: str, pr_number: int) -> Optional[str]:
    """
    Get the GraphQL node ID for a PR.

    Args:
        repo: Repository name (without organization)
        pr_number: PR number

    Returns:
        PR node ID string or None if the request failed
    """
    result = subprocess.run(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "-R",
            f"{GITHUB_ORGANIZATION}/{repo}",
            "--json",
            "id",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error(f"Failed to get PR details: {result.stderr}")
        return None

    pr_data = json.loads(result.stdout)
    return pr_data.get("id")


def approve_pr(repo: str, pr_number: int, message: str) -> bool:
    """
    Approve a pull request with a review message.

    Args:
        repo: Repository name (without organization)
        pr_number: PR number
        message: Review message to include with the approval

    Returns:
        True if approval succeeded, False otherwise
    """
    result = subprocess.run(
        [
            "gh",
            "pr",
            "review",
            str(pr_number),
            "-R",
            f"{GITHUB_ORGANIZATION}/{repo}",
            "--approve",
            "-b",
            message,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error(f"Failed to approve PR: {result.stderr}")
        return False

    log.info("[green]✓ Approved")
    return True


def add_pr_comment(repo: str, pr_number: int, message: str):
    """
    Add a comment to a pull request.

    Args:
        repo: Repository name (without organization)
        pr_number: PR number
        message: Comment message to add

    Returns:
        True if comment was added successfully, False otherwise
    """
    result = subprocess.run(
        [
            "gh",
            "pr",
            "comment",
            str(pr_number),
            "-R",
            f"{GITHUB_ORGANIZATION}/{repo}",
            "-b",
            message,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error(f"Failed to add comment: {result.stderr}")
        return False

    log.info("[green]✓ Comment added")
    return True


def merge_pr(repo: str, pr_number: int, merge_method: str = "squash") -> bool:
    """
    Merge a pull request immediately.

    Args:
        repo: Repository name (without organization)
        pr_number: PR number
        merge_method: Merge method to use (squash, merge, or rebase)

    Returns:
        True if merge succeeded, False otherwise
    """
    result = subprocess.run(
        [
            "gh",
            "pr",
            "merge",
            str(pr_number),
            "-R",
            f"{GITHUB_ORGANIZATION}/{repo}",
            f"--{merge_method}",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error(f"Failed to merge PR: {result.stderr}")
        return False

    log.info(f"[green]✓ Merged ({merge_method})")
    return True


def enable_auto_merge(repo: str, pr_number: int, merge_method: str = "SQUASH") -> bool:
    """
    Enable auto-merge for a pull request.

    Args:
        repo: Repository name (without organization)
        pr_number: PR number
        merge_method: Merge method to use (SQUASH, MERGE, or REBASE)

    Returns:
        True if auto-merge was enabled successfully, False otherwise
    """
    # First, get the PR node ID
    pr_node_id = get_pr_node_id(repo, pr_number)
    if not pr_node_id:
        return False

    # Enable auto-merge using GraphQL mutation
    mutation = """
    mutation($prId: ID!, $mergeMethod: PullRequestMergeMethod!) {
      enablePullRequestAutoMerge(input: {pullRequestId: $prId, mergeMethod: $mergeMethod}) {
        pullRequest {
          autoMergeRequest {
            enabledAt
          }
        }
      }
    }
    """

    result = subprocess.run(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={mutation}",
            "-F",
            f"prId={pr_node_id}",
            "-F",
            f"mergeMethod={merge_method}",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error(f"Failed to enable auto-merge: {result.stderr}")
        return False

    log.info(f"[green]✓ Auto-merge enabled ({merge_method.lower()})")
    return True

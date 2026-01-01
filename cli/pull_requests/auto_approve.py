import subprocess
from dataclasses import dataclass
from typing import Any, Optional, List, Tuple

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, Arg, PositionalArg
from hexagon.support.input.prompt import prompt
from hexagon.support.output.printer import log
from rich.panel import Panel
from rich.syntax import Syntax

from checks.check_gh_cli import check_gh_cli
from .diff_utils import (
    parse_diff_by_file,
    get_files_to_display,
)
from .github_cli_operations import (
    execute_graphql_query,
    get_pr_files,
    get_pr_diff,
    approve_pr as gh_approve_pr,
    enable_auto_merge as gh_enable_auto_merge,
    merge_pr as gh_merge_pr,
    add_pr_comment as gh_add_pr_comment,
    GITHUB_ORGANIZATION,
)

# Default approval message for dependency updates
DEFAULT_APPROVAL_MESSAGE = "LGTM!"

# Maximum lines to show per file in diff preview
MAX_DIFF_LINES_PER_FILE = 100

# GraphQL query for fetching chore(deps): PRs with all necessary metadata
DEPS_PRS_QUERY = """
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    pullRequests(first: 100, states: OPEN, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        number
        title
        url
        viewerDidAuthor
        reviewDecision
        autoMergeRequest {
          enabledAt
        }
        mergeable
        commits(last: 1) {
          nodes {
            commit {
              statusCheckRollup {
                state
              }
            }
          }
        }
        reviews(first: 100) {
          nodes {
            author {
              login
            }
            state
          }
        }
      }
    }
  }
  viewer {
    login
  }
}
"""


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class PRStatus:
    """Status information for a pull request."""

    is_already_approved: bool
    auto_merge_enabled: bool
    checks_status: str
    is_mergeable: bool
    checks_passing: bool
    is_ready: bool


@dataclass
class ProcessResult:
    """Result of processing a single PR."""

    pr_number: int
    pr_title: str
    pr_url: str
    was_approved: bool
    needs_attention: bool
    attention_reason: Optional[str] = None


def _pr_filter(pr) -> Any:
    return pr["title"].startswith("chore(deps):") or pr["title"].startswith(
        "chore(deps-dev):"
    )


class Args(ToolArgs):
    repository: PositionalArg[str] = Arg(
        None,
        prompt_message="Which REPOSITORY do you want to process?",
        searchable=True,
    )


def main(
    tool: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    check_gh_cli()

    log.panel(
        "This tool streamlines the process of reviewing and approving chore(deps): PRs by:\n"
        "1. Fetching all open chore(deps): PRs from a repository\n"
        "2. Showing diffs for each PR (skipping large lock files)\n"
        "3. Prompting for user approval\n"
        "4. Enabling auto-merge (before approval for immediate merge)\n"
        "5. Generating a Slack message for requesting second approvals\n",
        title="chore(deps): PR Auto-Approval Tool",
        color="yellow",
    )

    repo = "hexagon"
    dependency_prs, viewer_login = fetch_dependency_prs(repo)

    if not dependency_prs:
        log.info("[yellow]No chore(deps): PRs found in this repository.", gap_start=1)
        return

    log.info(f"Found [b]{len(dependency_prs)}[/] chore(deps): PR(s)", gap_end=1)

    approved_prs, need_attention_prs = process_all_prs(
        repo, dependency_prs, viewer_login
    )

    show_attention_summary(need_attention_prs)
    show_slack_message_for_ready_prs(repo, viewer_login)


def fetch_dependency_prs(repo: str) -> Tuple[List[dict], str]:
    """
    Fetch all open chore(deps): PRs from a repository.

    Args:
        repo: Repository name (without organization)

    Returns:
        Tuple of (List of PR dictionaries with metadata, viewer's GitHub login)
    """
    log.info(f"Fetching chore(deps): PRs from [b]{repo}[/]", gap_start=1)

    data = execute_graphql_query(
        DEPS_PRS_QUERY, {"owner": GITHUB_ORGANIZATION, "repo": repo}
    )

    if not data:
        return [], ""

    all_prs = data["data"]["repository"]["pullRequests"]["nodes"]
    viewer_login = data["data"]["viewer"]["login"]

    # Filter for chore(deps): PRs only
    dependency_prs = [pr for pr in all_prs if _pr_filter(pr)]

    return dependency_prs, viewer_login


def process_all_prs(
    repo: str, prs: List[dict], viewer_login: str
) -> Tuple[List[dict], List[dict]]:
    """
    Process all chore(deps): PRs, showing diffs and prompting for approval.

    Args:
        repo: Repository name
        prs: List of PR dictionaries to process
        viewer_login: Current user's GitHub login

    Returns:
        Tuple of (approved_prs, need_attention_prs)
        Each is a list of dictionaries with PR info
    """
    approved_prs = []
    need_attention_prs = []

    for pr in prs:
        result = process_single_pr(repo, pr, viewer_login)

        if result.was_approved:
            approved_prs.append(
                {
                    "number": result.pr_number,
                    "title": result.pr_title,
                    "url": result.pr_url,
                }
            )

        if result.needs_attention:
            need_attention_prs.append(
                {
                    "number": result.pr_number,
                    "title": result.pr_title,
                    "url": result.pr_url,
                    "reason": result.attention_reason,
                }
            )

    return approved_prs, need_attention_prs


def show_attention_summary(need_attention_prs: List[dict]):
    """
    Display a summary panel of PRs that need manual attention.

    Args:
        need_attention_prs: List of PRs with issues
    """
    if not need_attention_prs:
        return

    log.panel(
        "\n".join(
            [
                f"[b]PR #{pr['number']}:[/] {pr['title']}\n"
                f"{pr['url']}\n"
                f"[red]Reason: {pr['reason']}[/]"
                for pr in need_attention_prs
            ]
        ),
        title="⚠ PRs Needing Manual Attention",
        color="red",
    )


def show_slack_message_for_ready_prs(repo: str, viewer_login: str):
    """
    Re-check all PRs and generate Slack message for those ready for second approval.

    Args:
        repo: Repository name
        viewer_login: Current user's GitHub login
    """
    log.info("[cyan]Re-checking all chore(deps): PRs for Slack message...", gap_start=1)
    ready_for_second_approval = get_prs_ready_for_second_approval(repo, viewer_login)

    if ready_for_second_approval:
        generate_slack_message(repo, ready_for_second_approval)
    else:
        log.info("[yellow]No PRs currently waiting for second approval.")


# ============================================================================
# Single PR Processing
# ============================================================================


def process_single_pr(repo: str, pr: dict, viewer_login: str) -> ProcessResult:
    """
    Process a single PR: check status, show diff, prompt for approval.

    Args:
        repo: Repository name
        pr: PR dictionary with metadata
        viewer_login: Current user's GitHub login

    Returns:
        ProcessResult with outcome of processing
    """
    pr_number = pr["number"]
    pr_title = pr["title"]
    pr_url = pr["url"]

    # Get PR status
    status = get_pr_status_summary(pr, viewer_login)

    # Display PR status panel
    display_pr_status(pr_number, pr_title, pr_url, status)

    # Skip if viewer already approved (nothing more to do)
    if status.is_already_approved and status.checks_passing:
        log.info("[dim]Skipping this PR - you already approved it", gap_end=1)
        return ProcessResult(
            pr_number=pr_number,
            pr_title=pr_title,
            pr_url=pr_url,
            was_approved=False,
            needs_attention=False,
        )

    # Show diff for review
    show_pr_diff(repo, pr_number)

    # Prompt user for action
    actions = prompt_user_for_action(pr_number, status)

    if "skip" in actions:
        log.info("[dim]Skipping this PR", gap_end=1)
        return ProcessResult(
            pr_number=pr_number,
            pr_title=pr_title,
            pr_url=pr_url,
            was_approved=False,
            needs_attention=False,
        )

    # Execute the chosen action
    success = False
    if "merge" in actions:
        success = handle_merge_action(repo, pr_number)

    if not success:
        if "auto-merge" in actions:
            success = handle_auto_merge_action(repo, pr_number, status)

        if "rebase" in actions:
            success = handle_rebase_action(repo, pr_number)

    if success:
        log.info("[green]✓ Processed successfully", gap_end=1)

    return ProcessResult(
        pr_number=pr_number,
        pr_title=pr_title,
        pr_url=pr_url,
        was_approved=("merge" in actions or "auto-merge" in actions),
        needs_attention=False,
    )


# ============================================================================
# PR Status Checking
# ============================================================================


def get_pr_status_summary(pr: dict, viewer_login: str) -> PRStatus:
    """
    Extract and compute status information for a PR.

    Args:
        pr: PR dictionary from GraphQL query
        viewer_login: Current user's GitHub login

    Returns:
        PRStatus object with computed status fields
    """
    is_already_approved = viewer_did_approve(pr, viewer_login)
    auto_merge_enabled = pr.get("autoMergeRequest") is not None
    checks_status = get_checks_status(pr)
    is_mergeable = pr.get("mergeable") == "MERGEABLE"
    checks_passing = checks_status == "SUCCESS"
    is_ready = is_mergeable and checks_passing

    return PRStatus(
        is_already_approved=is_already_approved,
        auto_merge_enabled=auto_merge_enabled,
        checks_status=checks_status,
        is_mergeable=is_mergeable,
        checks_passing=checks_passing,
        is_ready=is_ready,
    )


def viewer_did_approve(pr: dict, viewer_login: str) -> bool:
    """
    Check if the current user (viewer) already approved this PR.

    Args:
        pr: PR dictionary from GraphQL query
        viewer_login: Current user's GitHub login

    Returns:
        True if viewer is the author or has already approved the PR
    """
    # If viewer is the author, they can't approve their own PR
    if pr.get("viewerDidAuthor"):
        return True

    # Check if viewer has already approved in the reviews
    reviews = pr.get("reviews", {}).get("nodes", [])
    for review in reviews:
        author = review.get("author")
        if author and author.get("login") == viewer_login:
            # Check if this review is an approval
            if review.get("state") == "APPROVED":
                return True

    return False


def get_checks_status(pr: dict) -> str:
    """
    Extract the CI checks status from a PR.

    Args:
        pr: PR dictionary from GraphQL query

    Returns:
        Status string: SUCCESS, PENDING, FAILED, or UNKNOWN
    """
    try:
        commits = pr.get("commits", {}).get("nodes", [])
        if not commits:
            return "UNKNOWN"

        commit = commits[0].get("commit", {})
        status_check_rollup = commit.get("statusCheckRollup")

        if not status_check_rollup:
            return "PENDING"

        state = status_check_rollup.get("state", "UNKNOWN")
        return state
    except (KeyError, IndexError, AttributeError):
        return "UNKNOWN"


def get_skip_reason(status: PRStatus) -> str:
    """
    Get a human-readable reason for skipping a PR.

    Args:
        status: PR status object

    Returns:
        Description of why the PR was skipped
    """
    if not status.checks_passing:
        return f"Checks: {status.checks_status}"
    elif not status.is_mergeable:
        return "Not mergeable (conflicts?)"
    else:
        return "Not ready"


# ============================================================================
# PR Display
# ============================================================================


def display_pr_status(pr_number: int, pr_title: str, pr_url: str, status: PRStatus):
    """
    Display a formatted panel showing PR status.

    Args:
        pr_number: PR number
        pr_title: PR title
        pr_url: PR URL
        status: PR status object
    """
    status_parts = format_status_parts(status)

    log.panel(
        f"[b]PR #{pr_number}:[/] {pr_title}\n"
        f"{pr_url}\n"
        f"Status: {' | '.join(status_parts)}",
        title="Processing PR",
        color="cyan" if status.is_ready else "yellow",
    )


def format_status_parts(status: PRStatus) -> List[str]:
    """
    Format status information into colored status strings.

    Args:
        status: PR status object

    Returns:
        List of formatted status strings
    """
    parts = []

    if status.is_already_approved:
        parts.append("[green]Already approved")
    else:
        parts.append("[yellow]Not approved")

    if status.auto_merge_enabled:
        parts.append("[green]Auto-merge enabled")
    else:
        parts.append("[yellow]Auto-merge disabled")

    if not status.checks_passing:
        parts.append(f"[red]Checks: {status.checks_status}")
    else:
        parts.append("[green]Checks: PASSING")

    return parts


# ============================================================================
# User Interaction
# ============================================================================


def prompt_user_for_action(pr_number: int, status: PRStatus) -> str:
    """
    Prompt user to choose an action for a PR.

    Args:
        pr_number: PR number
        status: PR status object

    Returns:
        Action string: "merge", "auto-merge", "rebase", or "skip"
    """
    # Build options based on PR readiness
    if status.is_ready:
        # PR is ready: no conflicts and all checks passed
        choices = [
            {
                "name": "Squash and merge now with default commit message",
                "value": "merge",
            },
            {
                "name": "Set auto-merge & approve (wait for second approval)",
                "value": "auto-merge",
            },
            {
                "name": 'Add comment "@dependabot rebase"',
                "value": "rebase",
            },
            {"name": "Skip this PR", "value": "skip"},
        ]
    else:
        # PR is not ready: has conflicts or checks haven't passed
        choices = [
            {
                "name": "Set auto-merge & approve (will merge when checks pass)",
                "value": "auto-merge",
            },
            {
                "name": 'Add comment "@dependabot rebase"',
                "value": "rebase",
            },
            {"name": "Skip this PR", "value": "skip"},
        ]

    return prompt.select(
        message=f"What would you like to do with PR #{pr_number}?",
        choices=choices,
        multiselect=True,
        default="merge" if status.is_ready else "auto-merge",
    )


# ============================================================================
# PR Actions
# ============================================================================


def handle_merge_action(repo: str, pr_number: int) -> bool:
    """
    Merge a PR immediately with squash method.

    Args:
        repo: Repository name
        pr_number: PR number

    Returns:
        True if merge succeeded, False otherwise
    """
    log.info(f"Merging PR #{pr_number} (squash)...")
    return gh_merge_pr(repo, pr_number, merge_method="squash")


def handle_auto_merge_action(repo: str, pr_number: int, status: PRStatus) -> bool:
    """
    Enable auto-merge and approve a PR (in that order).

    Auto-merge is enabled first so that the PR merges immediately
    when the second approval comes in.

    Args:
        repo: Repository name
        pr_number: PR number
        status: PR status object

    Returns:
        True if all actions succeeded, False otherwise
    """
    # Enable auto-merge FIRST (before approving)
    if not status.auto_merge_enabled:
        log.info(f"Enabling auto-merge (squash) for PR #{pr_number}...")
        if not gh_enable_auto_merge(repo, pr_number):
            log.info("[yellow]Skipping approval due to auto-merge failure", gap_end=1)
            return False
    else:
        log.info("[dim]Auto-merge already enabled")

    # Approve if not already approved
    if not status.is_already_approved:
        log.info(f"Approving PR #{pr_number}...")
        return gh_approve_pr(repo, pr_number, DEFAULT_APPROVAL_MESSAGE)
    else:
        log.info("[dim]Already approved, skipping approval")
        return True


def handle_rebase_action(repo: str, pr_number: int) -> bool:
    """
    Add a comment to request Dependabot to rebase the PR.

    Args:
        repo: Repository name
        pr_number: PR number

    Returns:
        True if comment was added successfully, False otherwise
    """
    log.info(f"Requesting rebase for PR #{pr_number}...")
    return gh_add_pr_comment(repo, pr_number, "@dependabot rebase")


# ============================================================================
# Diff Display
# ============================================================================


def show_pr_diff(repo: str, pr_number: int):
    """
    Display diff for a PR, showing each file separately and skipping large files.

    Args:
        repo: Repository name
        pr_number: PR number
    """
    files = fetch_pr_files_with_stats(repo, pr_number)
    if not files:
        log.info("[yellow]No files changed in this PR")
        return

    full_diff = get_pr_diff(repo, pr_number)
    if not full_diff:
        return

    file_diffs = parse_diff_by_file(full_diff)

    files_to_display, skipped_files = get_files_to_display(files)

    # Show skipped files
    for file_info in skipped_files:
        file_path = file_info["path"]
        additions = file_info.get("additions", 0)
        deletions = file_info.get("deletions", 0)
        reason = file_info.get("skip_reason", "")
        log.info(f"[dim]Skipping {reason}: {file_path} (+{additions}/-{deletions})")

    # Show diffs for displayable files
    for file_info in files_to_display:
        file_path = file_info["path"]
        additions = file_info.get("additions", 0)
        deletions = file_info.get("deletions", 0)

        file_diff = file_diffs.get(file_path)
        if not file_diff:
            continue

        display_file_diff(file_path, file_diff, additions, deletions)


def fetch_pr_files_with_stats(repo: str, pr_number: int) -> Optional[List[dict]]:
    """
    Fetch the list of files changed in a PR with their stats.

    Args:
        repo: Repository name
        pr_number: PR number

    Returns:
        List of file dictionaries or None on error
    """
    files = get_pr_files(repo, pr_number)
    if files is None:
        log.error("Failed to get PR files")
    return files


def display_file_diff(
    file_path: str, diff_content: str, additions: int, deletions: int
):
    """
    Display the diff for a single file in a formatted panel.

    Args:
        file_path: Path to the file
        diff_content: Unified diff content for the file
        additions: Number of lines added
        deletions: Number of lines deleted
    """
    lines = diff_content.split("\n")
    preview_lines = lines[:MAX_DIFF_LINES_PER_FILE]

    if len(lines) > MAX_DIFF_LINES_PER_FILE:
        preview_lines.append(
            f"\n... ({len(lines) - MAX_DIFF_LINES_PER_FILE} more lines)"
        )

    diff_text = "\n".join(preview_lines)

    log.extra(
        Panel(
            Syntax(diff_text, "diff", theme="monokai", line_numbers=False),
            title=f"[b]{file_path}[/b] (+{additions}/-{deletions})",
            border_style="blue",
        )
    )


# ============================================================================
# Slack Message Generation
# ============================================================================


def get_prs_ready_for_second_approval(repo: str, viewer_login: str) -> List[dict]:
    """
    Get all chore(deps): PRs that have checks passing and need exactly one more approval.

    This includes PRs where:
    - The viewer has already approved
    - Checks are passing
    - PR is mergeable
    - Auto-merge is enabled (waiting for second approval)
    - Still open (not merged yet)

    Args:
        repo: Repository name
        viewer_login: Current user's GitHub login

    Returns:
        List of PRs ready for second approval
    """
    dependency_prs, _ = fetch_dependency_prs(repo)
    ready_prs = []

    for pr in dependency_prs:
        # Only include PRs that the viewer has already approved
        if not viewer_did_approve(pr, viewer_login):
            continue

        checks_status = get_checks_status(pr)
        is_mergeable = pr.get("mergeable") == "MERGEABLE"
        checks_passing = checks_status == "SUCCESS"
        auto_merge_enabled = pr["autoMergeRequest"] is not None

        # Include if checks pass, mergeable, and auto-merge is enabled
        # (don't check reviewDecision because it only becomes APPROVED
        # after ALL required approvals, not just one)
        if checks_passing and is_mergeable and auto_merge_enabled:
            ready_prs.append(
                {
                    "number": pr["number"],
                    "title": pr["title"],
                    "url": pr["url"],
                }
            )

    return ready_prs


def generate_slack_message(repo: str, approved_prs: List[dict]):
    """
    Generate and display a Slack message for approved PRs.

    Args:
        repo: Repository name
        approved_prs: List of PRs that are approved and ready
    """
    log.panel(
        "PRs approved and ready for second review!",
        title="Slack Message",
        color="green",
    )

    message_content = build_slack_message_content(repo, approved_prs)
    display_and_copy_slack_message(message_content)


def build_slack_message_content(repo: str, prs: List[dict]) -> str:
    """
    Build the Slack message content.

    Args:
        repo: Repository name
        prs: List of PRs to include in message

    Returns:
        Formatted Slack message string
    """
    message_lines = [
        f"🤖 *chore(deps): PRs in `{repo}` ready for review*",
        "",
        "I've reviewed and approved these dependency update PRs. They need a second approval:",
        "",
    ]

    for pr in prs:
        message_lines.append(f"• <{pr['url']}|#{pr['number']}: {pr['title']}>")

    message_lines.extend(
        [
            "",
            "_Auto-merge is enabled, they'll merge automatically once approved._",
        ]
    )

    return "\n".join(message_lines)


def display_and_copy_slack_message(message: str):
    """
    Display the Slack message and attempt to copy it to clipboard.

    Args:
        message: Formatted Slack message
    """
    log.extra(
        Panel(
            message,
            border_style="green",
            padding=(1, 2),
        )
    )

    # Copy to clipboard if possible
    try:
        subprocess.run(
            ["pbcopy"],
            input=message,
            text=True,
            check=True,
        )
        log.info("[green]✓ Message copied to clipboard!", gap_end=1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        log.info(
            "[yellow]Could not copy to clipboard (pbcopy not available)", gap_end=1
        )

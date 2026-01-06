---
sidebar_position: 1
---

# Building a Custom Tool

This tutorial walks you through building a real custom tool for Hexagon. You'll learn how to create a tool that makes API requests, handles user input, and provides rich output.

## What We'll Build

We'll create a **GitHub Repository Info** tool that:
- Fetches information about a GitHub repository
- Accepts repository name as an argument
- Shows stars, forks, and description
- Handles errors gracefully
- Works with different GitHub API tokens per environment

## Prerequisites

- Hexagon installed
- A CLI project with `app.yaml` configuration
- Basic Python knowledge

## Step 1: Set Up Custom Tools Directory

First, configure your CLI to use a custom tools directory:

```yaml
# app.yaml
cli:
  name: My CLI
  command: mycli
  custom_tools_dir: ./custom_tools  # Add this line
```

Create the directory:

```bash
mkdir -p custom_tools
```

## Step 2: Create the Tool File

Create a new Python file for your tool:

```bash
touch custom_tools/github_info.py
```

## Step 3: Define Arguments

Start by defining the arguments your tool will accept:

```python
# custom_tools/github_info.py
from hexagon.support.input.args import ToolArgs, PositionalArg, OptionalArg, Arg

class Args(ToolArgs):
    """Arguments for the GitHub info tool."""

    repo: PositionalArg[str] = Arg(
        None,
        prompt_message="Enter repository (format: owner/repo)",
        description="GitHub repository in owner/repo format"
    )

    show_details: OptionalArg[bool] = Arg(
        False,
        alias="d",
        description="Show detailed information"
    )
```

**What's happening here:**
- `PositionalArg[str]`: Required argument that must be provided
- `OptionalArg[bool]`: Optional flag with default value
- `prompt_message`: Message shown if argument not provided
- `alias`: Short form for the argument (`--show-details` or `-d`)

## Step 4: Implement the Main Function

Add the main function that will execute when the tool runs:

```python
from hexagon.support.output.printer import log
import urllib.request
import json

def main(tool, env, env_args, cli_args: Args):
    """Fetch and display GitHub repository information.

    Args:
        tool: Tool configuration object
        env: Selected environment (or None)
        env_args: Environment-specific configuration
        cli_args: Parsed command-line arguments
    """
    # Prompt for repo if not provided
    if not cli_args.repo.value:
        cli_args.repo.prompt()

    # Validate repo format
    repo = cli_args.repo.value
    if "/" not in repo:
        log.error("Invalid repository format. Use: owner/repo")
        return ["Error: Invalid repository format"]

    # Show what we're doing
    log.info(f"Fetching information for: {repo}")

    # Make the API request
    try:
        url = f"https://api.github.com/repos/{repo}"

        # Add authentication token if provided via environment
        headers = {}
        if env_args and isinstance(env_args, dict) and "token" in env_args:
            headers["Authorization"] = f"token {env_args['token']}"

        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())

        # Extract key information
        name = data["full_name"]
        description = data["description"] or "No description"
        stars = data["stargazers_count"]
        forks = data["forks_count"]
        language = data["language"] or "Not specified"

        # Display results
        log.panel(
            f"**{name}**\n\n{description}",
            title="Repository Info"
        )

        results = [
            f"⭐ Stars: {stars:,}",
            f"🍴 Forks: {forks:,}",
            f"💻 Language: {language}"
        ]

        # Show additional details if requested
        if cli_args.show_details.value:
            results.extend([
                f"📅 Created: {data['created_at'][:10]}",
                f"📝 Updated: {data['updated_at'][:10]}",
                f"🐛 Open Issues: {data['open_issues_count']}"
            ])

        return results

    except urllib.error.HTTPError as e:
        if e.code == 404:
            log.error(f"Repository not found: {repo}")
            return [f"Error: Repository '{repo}' not found"]
        elif e.code == 403:
            log.error("API rate limit exceeded. Use a GitHub token.")
            return ["Error: API rate limit exceeded"]
        else:
            log.error(f"GitHub API error: {e.code}")
            return [f"Error: GitHub API returned {e.code}"]

    except Exception as e:
        log.error(f"Unexpected error: {str(e)}")
        return [f"Error: {str(e)}"]
```

## Step 5: Add Tool to Configuration

Now add your tool to `app.yaml`:

```yaml
tools:
  - name: github-info
    alias: gh
    long_name: GitHub Repository Info
    description: Get information about a GitHub repository
    type: shell
    action: github_info
```

## Step 6: Test Your Tool

Test the basic functionality:

```bash
# With repo as argument
mycli github-info facebook/react

# Without argument (will prompt)
mycli github-info

# With details flag
mycli github-info facebook/react --show-details
```

You should see output like:

```
Fetching information for: facebook/react

┌─ Repository Info ────────────────────────────┐
│ **facebook/react**                           │
│                                              │
│ The library for web and native interfaces   │
└──────────────────────────────────────────────┘

⭐ Stars: 230,000
🍴 Forks: 47,000
💻 Language: JavaScript
```

## Step 7: Add Environment Support

Let's add support for different GitHub tokens per environment:

```yaml
envs:
  - name: personal
    alias: p
  - name: work
    alias: w

tools:
  - name: github-info
    alias: gh
    long_name: GitHub Repository Info
    description: Get information about a GitHub repository
    type: shell
    action: github_info
    envs:
      personal:
        token: "ghp_your_personal_token"
      work:
        token: "ghp_your_work_token"
```

Now you can use different tokens based on the environment:

```bash
# Use personal token
mycli github-info personal facebook/react

# Use work token
mycli github-info work your-company/private-repo
```

## Step 8: Improve Error Handling

Let's add better validation and error messages:

```python
def validate_repo_format(repo: str) -> bool:
    """Validate that repo is in owner/repo format."""
    if "/" not in repo:
        return False

    parts = repo.split("/")
    if len(parts) != 2:
        return False

    owner, name = parts
    if not owner or not name:
        return False

    return True

def main(tool, env, env_args, cli_args: Args):
    # Prompt for repo if not provided
    if not cli_args.repo.value:
        cli_args.repo.prompt()

    # Validate format
    repo = cli_args.repo.value
    if not validate_repo_format(repo):
        log.error("Invalid repository format")
        log.info("Expected format: owner/repo")
        log.example("mycli github-info facebook/react")
        return ["Error: Invalid repository format"]

    # Rest of the implementation...
```

## Step 9: Add Interactive Suggestions

Make the tool more user-friendly with suggestions:

```python
class Args(ToolArgs):
    repo: PositionalArg[str] = Arg(
        None,
        prompt_message="Enter repository (format: owner/repo)",
        prompt_suggestions=[
            "facebook/react",
            "microsoft/vscode",
            "vercel/next.js",
            "vuejs/vue"
        ],
        searchable=True,
        description="GitHub repository in owner/repo format"
    )

    show_details: OptionalArg[bool] = Arg(
        False,
        alias="d",
        description="Show detailed information"
    )
```

Now when users are prompted, they'll see popular repositories as suggestions they can select or search through.

## Complete Code

Here's the complete tool implementation:

```python
# custom_tools/github_info.py
from hexagon.support.output.printer import log
from hexagon.support.input.args import ToolArgs, PositionalArg, OptionalArg, Arg
import urllib.request
import json

class Args(ToolArgs):
    """Arguments for the GitHub info tool."""

    repo: PositionalArg[str] = Arg(
        None,
        prompt_message="Enter repository (format: owner/repo)",
        prompt_suggestions=[
            "facebook/react",
            "microsoft/vscode",
            "vercel/next.js",
            "vuejs/vue"
        ],
        searchable=True,
        description="GitHub repository in owner/repo format"
    )

    show_details: OptionalArg[bool] = Arg(
        False,
        alias="d",
        description="Show detailed information"
    )

def validate_repo_format(repo: str) -> bool:
    """Validate that repo is in owner/repo format."""
    if "/" not in repo:
        return False

    parts = repo.split("/")
    if len(parts) != 2:
        return False

    owner, name = parts
    if not owner or not name:
        return False

    return True

def main(tool, env, env_args, cli_args: Args):
    """Fetch and display GitHub repository information.

    Args:
        tool: Tool configuration object
        env: Selected environment (or None)
        env_args: Environment-specific configuration
        cli_args: Parsed command-line arguments
    """
    # Prompt for repo if not provided
    if not cli_args.repo.value:
        cli_args.repo.prompt()

    # Validate format
    repo = cli_args.repo.value
    if not validate_repo_format(repo):
        log.error("Invalid repository format")
        log.info("Expected format: owner/repo")
        log.example("mycli github-info facebook/react")
        return ["Error: Invalid repository format"]

    # Show what we're doing
    log.info(f"Fetching information for: {repo}")

    # Make the API request
    try:
        url = f"https://api.github.com/repos/{repo}"

        # Add authentication token if provided via environment
        headers = {}
        if env_args and isinstance(env_args, dict) and "token" in env_args:
            headers["Authorization"] = f"token {env_args['token']}"

        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())

        # Extract key information
        name = data["full_name"]
        description = data["description"] or "No description"
        stars = data["stargazers_count"]
        forks = data["forks_count"]
        language = data["language"] or "Not specified"

        # Display results
        log.panel(
            f"**{name}**\n\n{description}",
            title="Repository Info"
        )

        results = [
            f"⭐ Stars: {stars:,}",
            f"🍴 Forks: {forks:,}",
            f"💻 Language: {language}"
        ]

        # Show additional details if requested
        if cli_args.show_details.value:
            results.extend([
                f"📅 Created: {data['created_at'][:10]}",
                f"📝 Updated: {data['updated_at'][:10]}",
                f"🐛 Open Issues: {data['open_issues_count']}"
            ])

        return results

    except urllib.error.HTTPError as e:
        if e.code == 404:
            log.error(f"Repository not found: {repo}")
            return [f"Error: Repository '{repo}' not found"]
        elif e.code == 403:
            log.error("API rate limit exceeded. Use a GitHub token.")
            return ["Error: API rate limit exceeded"]
        else:
            log.error(f"GitHub API error: {e.code}")
            return [f"Error: GitHub API returned {e.code}"]

    except Exception as e:
        log.error(f"Unexpected error: {str(e)}")
        return [f"Error: {str(e)}"]
```

## Key Takeaways

**Arguments:**
- Use `PositionalArg` for required parameters
- Use `OptionalArg` for optional flags and parameters
- Always use `.value` to access the actual argument value
- Add `prompt_suggestions` for better UX

**Error Handling:**
- Catch specific exceptions (HTTPError, FileNotFoundError, etc.)
- Provide helpful error messages
- Use `log.error()` for user-facing errors
- Return error strings in the results list

**Output:**
- Use `log.info()` for progress messages
- Use `log.panel()` for highlighted information
- Return list of strings for final results
- Use emojis for visual appeal (optional)

**Environment Support:**
- Use `env_args` for environment-specific configuration
- Check if `env_args` exists before using it
- Common use cases: API tokens, URLs, configuration

## Next Steps

Now that you've built a custom tool, explore:

- [Prompting Guide](../advanced/prompting) - Advanced interactive features
- [Custom Tools Reference](../advanced/custom-tools) - Complete API documentation
- [Output API](../api/support/output) - Rich terminal output options
- [Storage API](../api/support/storage) - Persisting data between runs

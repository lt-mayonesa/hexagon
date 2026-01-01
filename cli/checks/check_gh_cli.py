import subprocess
import sys

from hexagon.support.output.printer import log


def check_gh_cli():
    """Check if gh CLI is installed and authenticated"""
    if not _is_gh_installed():
        log.panel(
            "GitHub CLI (gh) is not installed. Please install it first:\n"
            "  [b]brew install gh[/b]\n"
            "\n"
            "Then authenticate with: [b]gh auth login[/b]",
            color="red",
            title="GitHub CLI Not Found",
        )
        sys.exit(1)

    if not _is_gh_authenticated():
        log.panel(
            "You are not authenticated with GitHub CLI.\n"
            "\n"
            "Please run: [b]gh auth login[/b]",
            color="red",
            title="GitHub CLI Authentication Required",
        )
        sys.exit(1)


def _is_gh_installed() -> bool:
    """Check if gh CLI is installed"""
    try:
        subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _is_gh_authenticated() -> bool:
    """Check if gh CLI is authenticated"""
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0

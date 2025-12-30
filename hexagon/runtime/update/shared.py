import datetime
import os
import re
import subprocess
import sys
from typing import Optional, Tuple

from packaging.version import Version

from hexagon.runtime.singletons import options
from hexagon.support.storage import (
    HexagonStorageKeys,
    load_user_data,
    store_user_data,
)

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"


def already_checked_for_updates(app: str = None) -> bool:
    last_checked = load_user_data(HexagonStorageKeys.last_update_check.value, app)

    result = False

    if last_checked:
        last_checked_date = datetime.datetime.strptime(
            last_checked, LAST_UPDATE_DATE_FORMAT
        )

        result = (
            last_checked_date + options.update_time_between_checks
            >= datetime.datetime.now()
        )

    if not result:
        store_user_data(
            HexagonStorageKeys.last_update_check.value,
            datetime.date.today().strftime(LAST_UPDATE_DATE_FORMAT),
            app=app,
        )

    return result


def check_hexagon_version() -> Tuple[Version, Version]:
    """
    Check current and latest hexagon versions.

    Returns:
        Tuple of (current_version, latest_version)
    """
    from hexagon.runtime.update import version

    current_version = version.local(
        override=os.getenv("HEXAGON_TEST_LOCAL_VERSION_OVERRIDE", None)
    )
    latest_version = version.latest(
        override=os.getenv("HEXAGON_TEST_LATEST_VERSION_OVERRIDE", None)
    )
    return current_version, latest_version


def perform_hexagon_update() -> None:
    """Execute pip upgrade command for hexagon."""
    subprocess.check_call(
        f"{sys.executable} -m pip install hexagon --upgrade",
        shell=True,
        stdout=subprocess.DEVNULL,
    )


def get_hexagon_changelog(current_version: Version) -> str:
    """
    Fetch and parse changelog from GitHub.

    Args:
        current_version: Current hexagon version

    Returns:
        Formatted changelog string
    """
    from hexagon.runtime.update import REPO_ORG, REPO_NAME
    from hexagon.runtime.update.changelog.fetch import fetch_changelog
    from hexagon.runtime.update.changelog.parse import parse_changelog

    return parse_changelog(current_version, fetch_changelog(REPO_ORG, REPO_NAME))


def check_cli_version() -> Tuple[bool, Optional[str]]:
    """
    Check if CLI needs update.

    Returns:
        Tuple of (needs_update, current_branch)
    """
    from hexagon.runtime.update.cli.command import (
        execute_command_in_cli_project_path,
        output_from_command_in_cli_project_path,
    )
    from hexagon.runtime.update.cli.git import load_cli_git_config

    cli_git_config = load_cli_git_config()
    if not cli_git_config:
        return False, None

    current_branch_status = output_from_command_in_cli_project_path("git status")
    current_branch_match = re.search(r"On branch (.+)", current_branch_status)
    if not current_branch_match:
        return False, None
    current_branch = current_branch_match.group(1)

    execute_command_in_cli_project_path("git remote update")
    branch_status = output_from_command_in_cli_project_path("git status -uno")

    needs_update = "is behind" in branch_status
    return needs_update, current_branch


def perform_cli_update() -> None:
    """Execute git pull and scan dependencies."""
    from hexagon.runtime.dependencies import scan_and_install_dependencies
    from hexagon.runtime.singletons import configuration
    from hexagon.runtime.update.cli.command import execute_command_in_cli_project_path

    execute_command_in_cli_project_path("git pull", show_stdout=True)
    scan_and_install_dependencies(configuration.custom_tools_path)

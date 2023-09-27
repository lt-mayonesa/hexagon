import re
import sys

from hexagon.runtime.dependencies import scan_and_install_dependencies
from hexagon.runtime.singletons import cli, configuration, options
from hexagon.runtime.update.cli.command import (
    execute_command_in_cli_project_path,
    output_from_command_in_cli_project_path,
)
from hexagon.runtime.update.cli.git import load_cli_git_config
from hexagon.runtime.update.shared import already_checked_for_updates
from hexagon.runtime.update.silent_fail import silent_fail
from hexagon.support.input.prompt import prompt
from hexagon.support.output.printer import log


@silent_fail
def check_for_cli_updates():
    if options.cli_update_disabled:
        return
    if already_checked_for_updates():
        return

    with log.status(_("msg.support.update.cli.checking_for_cli_updates")) as status:
        cli_git_config = load_cli_git_config()
        if not cli_git_config:
            return

        status.update(
            _("msg.support.update.cli.checking_for_cli_updates_on_branch").format(
                branch=_current_branch()
            )
        )

        if "is behind" in _get_updated_branch_status():
            log.info(
                _("msg.support.update.cli.new_version_available").format(
                    cli_name=cli.name
                )
            )
            if not prompt.confirm(
                _("action.support.update.cli.confirm_update"), default=True
            ):
                return

            _update_branch()
            scan_and_install_dependencies(configuration.custom_tools_path)

            log.info(_("msg.support.update.cli.updated"))
            log.finish()
            sys.exit(0)


def _current_branch():
    current_git_branch_status = output_from_command_in_cli_project_path("git status")
    return re.search(r"On branch (.+)", current_git_branch_status).groups(0)[0]


def _get_updated_branch_status():
    execute_command_in_cli_project_path("git remote update")
    branch_status = output_from_command_in_cli_project_path("git status -uno")
    return branch_status


def _update_branch():
    execute_command_in_cli_project_path("git pull", show_stdout=True)

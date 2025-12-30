import sys

from hexagon.runtime.singletons import cli
from hexagon.runtime.update.shared import check_cli_version, perform_cli_update
from hexagon.support.input.prompt import prompt
from hexagon.support.output.printer import log


def main(tool, env, env_args, cli_args):
    """
    Manually check for and install CLI updates.

    This bypasses time throttle and always checks git for updates.
    Prompts for confirmation before updating.
    """
    with log.status(_("msg.support.update.cli.checking_for_cli_updates")) as status:
        needs_update, current_branch = check_cli_version()

        if not needs_update:
            if current_branch:
                log.info(
                    _("msg.actions.internal.update_cli.already_latest").format(
                        cli_name=cli.name, branch=current_branch
                    )
                )
            else:
                log.info(
                    _("msg.actions.internal.update_cli.no_git_config").format(
                        cli_name=cli.name
                    )
                )
            return

        status.update(
            _("msg.support.update.cli.checking_for_cli_updates_on_branch").format(
                branch=current_branch
            )
        )

    log.info(
        _("msg.support.update.cli.new_version_available").format(cli_name=cli.name)
    )

    if not prompt.confirm(_("action.support.update.cli.confirm_update"), default=True):
        log.info(_("msg.actions.internal.update_cli.cancelled"))
        return

    with log.status(_("msg.support.update.cli.updating")):
        perform_cli_update()

    log.info(_("msg.support.update.cli.updated"))
    log.finish()
    sys.exit(0)

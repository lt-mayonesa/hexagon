import sys

from hexagon.runtime.singletons import cli, options
from hexagon.runtime.update.shared import (
    already_checked_for_updates,
    check_cli_version,
    perform_cli_update,
)
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
        needs_update, current_branch = check_cli_version()

        if not needs_update:
            return

        status.update(
            _("msg.support.update.cli.checking_for_cli_updates_on_branch").format(
                branch=current_branch
            )
        )

        log.info(
            _("msg.support.update.cli.new_version_available").format(cli_name=cli.name)
        )

        if not prompt.confirm(
            _("action.support.update.cli.confirm_update"), default=True
        ):
            return

        with log.status(_("msg.support.update.cli.updating")):
            perform_cli_update()

        log.info(_("msg.support.update.cli.updated"))
        log.finish()
        sys.exit(0)

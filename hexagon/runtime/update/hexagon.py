import os
import sys

from hexagon.runtime.singletons import options
from hexagon.runtime.update.shared import (
    already_checked_for_updates,
    check_hexagon_version,
    get_hexagon_changelog,
    perform_hexagon_update,
)
from hexagon.runtime.update.silent_fail import silent_fail
from hexagon.support.input.prompt import prompt
from hexagon.support.output.printer import log
from hexagon.support.storage import HEXAGON_STORAGE_APP


@silent_fail
def check_for_hexagon_updates():
    if options.update_disabled:
        return
    if already_checked_for_updates(HEXAGON_STORAGE_APP):
        return

    with log.status(_("msg.support.update.hexagon.checking_new_versions")):
        current_version, latest_version = check_hexagon_version()

        if current_version >= latest_version:
            return

        log.info(
            _("msg.support.update.hexagon.new_version_available").format(
                latest_version=latest_version
            )
        )

        if bool(os.getenv("HEXAGON_UPDATE_SHOW_CHANGELOG", "1")):
            with log.status(_("msg.support.update.hexagon.fetching_changelog")):
                changelog = get_hexagon_changelog(current_version)

            log.example(changelog, syntax="md")

        if not prompt.confirm(
            _("action.support.update.hexagon.confirm_update"), default=True
        ):
            return

        with log.status(_("msg.support.update.hexagon.updating")):
            perform_hexagon_update()

        log.info(_("msg.support.update.hexagon.updated"))
        log.finish()
        sys.exit(1)

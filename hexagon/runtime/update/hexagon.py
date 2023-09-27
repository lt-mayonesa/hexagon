import os
import subprocess
import sys

from hexagon.runtime.singletons import options
from hexagon.runtime.update import REPO_ORG, REPO_NAME
from hexagon.runtime.update import version
from hexagon.runtime.update.changelog.fetch import fetch_changelog
from hexagon.runtime.update.changelog.format import format_entries
from hexagon.runtime.update.changelog.parse import parse_changelog
from hexagon.runtime.update.shared import already_checked_for_updates
from hexagon.runtime.update.silent_fail import silent_fail
from hexagon.support.input.prompt import prompt
from hexagon.support.output.printer import log
from hexagon.support.storage import HEXAGON_STORAGE_APP

CHANGELOG_MAX_PRINT_ENTRIES = 10


@silent_fail
def check_for_hexagon_updates():
    if options.update_disabled:
        return
    if already_checked_for_updates(HEXAGON_STORAGE_APP):
        return

    with log.status(_("msg.support.update.hexagon.checking_new_versions")):
        current_version = version.local(
            override=os.getenv("HEXAGON_TEST_VERSION_OVERRIDE", None)
        )
        latest_version = version.latest()

        if current_version >= latest_version:
            return

        log.info(
            _("msg.support.update.hexagon.new_version_available").format(
                latest_version=latest_version
            )
        )

        if bool(os.getenv("HEXAGON_UPDATE_SHOW_CHANGELOG", "1")):
            with log.status(_("msg.support.update.hexagon.fetching_changelog")):
                changelog = parse_changelog(
                    current_version, fetch_changelog(REPO_ORG, REPO_NAME)
                )

            entries = format_entries(changelog)

            for entry in entries[:CHANGELOG_MAX_PRINT_ENTRIES]:
                log.info("  - " + entry.message)

            if len(entries) > CHANGELOG_MAX_PRINT_ENTRIES:
                log.info(_("msg.support.update.hexagon.and_much_more"))

        if not prompt.confirm(
            _("action.support.update.hexagon.confirm_update"), default=True
        ):
            return

        with log.status(_("msg.support.update.hexagon.updating")):
            subprocess.check_call(
                f"{sys.executable} -m pip --disable-pip-version-check install https://github.com/{REPO_ORG}/{REPO_NAME}/releases/download/v{latest_version}/hexagon-{latest_version}.tar.gz",
                shell=True,
                stdout=subprocess.DEVNULL,
            )

        log.info(_("msg.support.update.hexagon.updated"))
        log.finish()
        sys.exit(1)

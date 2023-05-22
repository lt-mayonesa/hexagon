import os
import subprocess
import sys

from hexagon.domain.singletons import options
from hexagon.support.printer import log
from hexagon.support.prompt import prompt
from hexagon.support.storage import HEXAGON_STORAGE_APP
from hexagon.support.update import REPO_ORG, REPO_NAME, version
from hexagon.support.update.changelog.fetch import fetch_changelog
from hexagon.support.update.changelog.format import format_entries
from hexagon.support.update.changelog.parse import parse_changelog
from hexagon.support.update.shared import already_checked_for_updates

CHANGELOG_MAX_PRINT_ENTRIES = 10


def check_for_hexagon_updates():
    if options.update_disabled:
        return
    if already_checked_for_updates(HEXAGON_STORAGE_APP):
        return

    current_version = version.local()
    with log.status(_("msg.support.update.hexagon.checking_new_versions")):
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

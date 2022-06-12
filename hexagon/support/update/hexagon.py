import json
import os
import subprocess
import sys
from urllib.request import Request, urlopen

import pkg_resources
from InquirerPy import inquirer
from packaging.version import parse as parse_version

from hexagon.support.github import add_github_access_token
from hexagon.support.printer import log
from hexagon.support.storage import HEXAGON_STORAGE_APP
from hexagon.support.update import REPO_ORG, REPO_NAME
from hexagon.support.update.changelog.format import format_entries
from hexagon.support.update.changelog.parse import parse_changelog
from hexagon.support.update.changelog.fetch import fetch_changelog
from hexagon.support.update.shared import already_checked_for_updates

CHANGELOG_MAX_PRINT_ENTRIES = 10


def check_for_hexagon_updates():
    if bool(os.getenv("HEXAGON_UPDATE_DISABLED")):
        return
    if already_checked_for_updates(HEXAGON_STORAGE_APP):
        return

    current_version = parse_version(
        os.getenv("HEXAGON_TEST_VERSION_OVERRIDE")
        if "HEXAGON_TEST_VERSION_OVERRIDE" in os.environ
        else pkg_resources.require("hexagon")[0].version
    )
    latest_github_release_version = _latest_github_release()

    if current_version >= parse_version(latest_github_release_version):
        return

    log.info(
        _("msg.support.update.hexagon.new_version_available").format(
            latest_version=latest_github_release_version
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

    if not inquirer.confirm(
        _("action.support.update.hexagon.confirm_update"), default=True
    ).execute():
        return

    with log.status(_("msg.support.update.hexagon.updating")):
        subprocess.check_call(
            f"{sys.executable} -m pip --disable-pip-version-check install https://github.com/{REPO_ORG}/{REPO_NAME}/releases/download/v{latest_github_release_version}/hexagon-{latest_github_release_version}.tar.gz",
            shell=True,
            stdout=subprocess.DEVNULL,
        )

    log.info(_("msg.support.update.hexagon.updated"))
    log.finish()
    sys.exit(1)


def _latest_github_release():
    with log.status(_("msg.support.update.hexagon.checking_new_versions")):
        latest_release_request = Request(
            f"https://api.github.com/repos/{REPO_ORG}/{REPO_NAME}/releases/latest"
        )
        add_github_access_token(latest_release_request)
        latest_github_release = json.load(urlopen(latest_release_request))
        return latest_github_release["name"].replace("v", "")

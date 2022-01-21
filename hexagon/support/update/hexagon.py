from hexagon.support.storage import HEXAGON_STORAGE_APP
from hexagon.support.update.shared import already_checked_for_updates
from hexagon.support.github import add_github_access_token
import re
from typing import List, Optional
import pkg_resources
import json
import os
import subprocess
import sys
from urllib.request import Request, urlopen
from packaging.version import parse as parse_version, Version
from markdown import Markdown
from io import StringIO
from hexagon.support.printer import log, translator
from InquirerPy import inquirer
from functools import reduce

_ = translator

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"
REPO_ORG = "redbeestudios"
REPO_NAME = "hexagon"
CHANGELOG_TYPE_FEATURE = "Feature"
CHANGELOG_TYPE_FIX = "Fix"
CHANGELOG_TYPE_DOCUMENTATION = "Documentation"
CHANGELOG_MAX_ENTRIES = 10
CHANGELOG_ENTRY_TYPE_ORDER_MAP = {
    CHANGELOG_TYPE_FEATURE: 2,
    CHANGELOG_TYPE_FIX: 1,
    CHANGELOG_TYPE_DOCUMENTATION: 0,
}
CHANGELOG_MAX_EMPTY_LINES = 10


class ChangelogEntry:
    def __init__(self, type: str, message: str):
        self.type = type
        self.message = message

    type: str
    message: str


class ChangelogVersionEntry:
    def __init__(self, version: str):
        self.version = version
        self.entries = []

    version: str
    entries: List[ChangelogEntry]


# TODO: Move changelog logic to its own module in the update module
def _parse_changelog(
    current_hexagon_version: Version, repo_org: str, repo_name: str
) -> List[ChangelogVersionEntry]:
    request = Request(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/contents/CHANGELOG.md"
    )
    request.add_header("Accept", "application/vnd.github.3.raw")
    add_github_access_token(request)
    changelog_file_path = os.getenv("HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE")
    consecutive_empty_lines_count = 0
    with open(changelog_file_path, "r") if changelog_file_path else urlopen(
        request
    ) as changelog_file:
        entries = []
        current_version: Optional[ChangelogVersionEntry] = None
        current_entry_type: str
        while True:
            readed_line = changelog_file.readline()
            line = (
                readed_line
                if changelog_file_path
                else readed_line.decode(changelog_file.headers.get_content_charset())
            )

            version_match = re.search("^## v(\\d+\\.\\d+\\.\\d+)", line)
            if version_match:
                if current_version:
                    entries.append(current_version)
                current_version = ChangelogVersionEntry(version_match.groups(0)[0])
                if current_hexagon_version == parse_version(current_version.version):
                    entries.append(current_version)
                    break

            entry_type_match = re.search("^### (\\w+)$", line)
            if entry_type_match:
                current_entry_type = entry_type_match.groups(0)[0]

            match = re.search("^\\* ([^(]+)", line)
            if match:
                current_version.entries.append(
                    ChangelogEntry(current_entry_type, match.groups(0)[0])
                )

            if not line:
                if consecutive_empty_lines_count > CHANGELOG_MAX_EMPTY_LINES:
                    entries.append(current_version)
                    break
                else:
                    consecutive_empty_lines_count += 1
            else:
                consecutive_empty_lines_count = 0

        return entries


def _unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        _unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = _unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def _unmark(text):
    return __md.convert(text)


def _show_changelog(current_hexagon_version: Version):
    if bool(os.getenv("HEXAGON_UPDATE_SHOW_CHANGELOG", "1")):

        with log.status(_("msg.support.update.hexagon.fetching_changelog")):
            changelog = _parse_changelog(current_hexagon_version, REPO_ORG, REPO_NAME)

        if changelog:

            def reducer(acc: List[ChangelogEntry], version: ChangelogVersionEntry):
                acc.extend(version.entries)
                return acc

            entries = reduce(reducer, changelog, [])
            entries.sort(
                key=lambda e: CHANGELOG_ENTRY_TYPE_ORDER_MAP[e.type], reverse=True
            )
            for entry in entries[:CHANGELOG_MAX_ENTRIES]:
                log.info("  - " + _unmark(entry.message))
            if len(entries) > CHANGELOG_MAX_ENTRIES:
                log.info(_("msg.support.update.hexagon.and_much_more"))


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

    # FIXME find a better way of handling colors in translations
    log.info(
        _("msg.support.update.hexagon.new_version_available").format(
            latest_version=latest_github_release_version,
            hexagon_start="[cyan]",
            hexagon_end="[/cyan]",
            version_start="[green]",
            version_end="[/green]",
        )
    )

    _show_changelog(current_version)

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

    log.info(
        "[green]{}️[white]{}".format(
            _("icon.global.ok"), _("msg.support.update.hexagon.updated")
        )
    )
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

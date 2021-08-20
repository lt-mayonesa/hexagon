from hexagon.support.github import add_github_access_token
import re
from typing import List
import pkg_resources
import json
import os
import subprocess
import sys
from urllib.request import Request, urlopen
from packaging.version import parse as parse_version, Version
from markdown import Markdown
from io import StringIO
from hexagon.support.printer import log
from hexagon.support.storage import (
    store_user_data,
    load_user_data,
    HEXAGON_STORAGE_APP,
    HexagonStorageKeys,
)
from InquirerPy import inquirer
import datetime
from halo import Halo
from functools import reduce

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


def __already_checked():
    last_checked = load_user_data(
        HexagonStorageKeys.last_update_check.value, HEXAGON_STORAGE_APP
    )

    result = False

    if last_checked:
        last_checked_date = datetime.datetime.strptime(
            last_checked, LAST_UPDATE_DATE_FORMAT
        ).date()

        # TODO: Move to hexagon configuration
        # See https://github.com/redbeestudios/hexagon/pull/35#discussion_r670870804 for more information
        result = last_checked_date >= datetime.date.today()

    if not result:
        store_user_data(
            HexagonStorageKeys.last_update_check.value,
            datetime.date.today().strftime(LAST_UPDATE_DATE_FORMAT),
            app=HEXAGON_STORAGE_APP,
        )

    return result


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
        current_version: ChangelogVersionEntry = None
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


def unmark(text):
    return __md.convert(text)


def _show_changelog(
    current_hexagon_version: Version,
    spinners_disabled: bool,
):
    if bool(os.getenv("HEXAGON_UPDATE_SHOW_CHANGELOG", "1")):
        changelog = None

        def get_changelog():
            return _parse_changelog(current_hexagon_version, REPO_ORG, REPO_NAME)

        if spinners_disabled:
            changelog = get_changelog()
        else:
            with Halo(text="Loading changelog"):
                changelog = get_changelog()

        if changelog:

            def reducer(acc: List[ChangelogEntry], version: ChangelogVersionEntry):
                acc.extend(version.entries)
                return acc

            entries = reduce(reducer, changelog, [])
            entries.sort(
                key=lambda entry: CHANGELOG_ENTRY_TYPE_ORDER_MAP[entry.type],
                reverse=True,
            )
            for entry in entries[:CHANGELOG_MAX_ENTRIES]:
                log.info("  - " + unmark(entry.message))
            if len(entries) > CHANGELOG_MAX_ENTRIES:
                log.info("and much more!")


def check_for_hexagon_updates():
    if bool(os.getenv("HEXAGON_UPDATE_DISABLED")):
        return
    if __already_checked():
        return

    current_version = parse_version(
        os.getenv(
            "HEXAGON_TEST_VERSION_OVERRIDE", pkg_resources.require("hexagon")[0].version
        )
    )

    latest_release_request = Request(
        f"https://api.github.com/repos/{REPO_ORG}/{REPO_NAME}/releases/latest"
    )
    add_github_access_token(latest_release_request)
    latest_github_release = json.load(urlopen(latest_release_request))
    latest_github_release_version = latest_github_release["name"].replace("v", "")

    if current_version >= parse_version(latest_github_release_version):
        return

    log.info(
        f"New [cyan]hexagon [white]version available [green]{latest_github_release_version}[white]!"
    )

    spinners_disabled = bool(os.getenv("HEXAGON_DISABLE_SPINNER", ""))

    _show_changelog(current_version, spinners_disabled)

    if not inquirer.confirm("Would you like to update?", default=True).execute():
        return

    def update():
        subprocess.check_call(
            f"{sys.executable} -m pip --disable-pip-version-check install https://github.com/{REPO_ORG}/{REPO_NAME}/releases/download/v{latest_github_release_version}/hexagon-{latest_github_release_version}.tar.gz",
            shell=True,
            stdout=subprocess.DEVNULL,
        )

    if spinners_disabled:
        update()
    else:
        with Halo(text="Updating"):
            update()

    log.info("[green]✔️ [white]Updated to latest version")
    log.finish()
    sys.exit(1)

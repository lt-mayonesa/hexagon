import re
from io import StringIO
from typing import List, Optional

from markdown import Markdown
from packaging.version import parse as parse_version, Version

from hexagon.runtime.update.changelog import ChangelogVersionEntry, ChangelogEntry
from hexagon.runtime.update.changelog.fetch import ChangelogFile

CHANGELOG_MAX_EMPTY_LINES = 10


def parse_changelog(
    current_hexagon_version: Version, changelog_file: ChangelogFile
) -> List[ChangelogVersionEntry]:
    entries = []
    current_version: Optional[ChangelogVersionEntry] = None
    current_entry_type: str = ""
    consecutive_empty_lines_count = 0
    while True:
        line = changelog_file.line()

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
                ChangelogEntry(current_entry_type, _unmark(match.groups(0)[0]))
            )

        if not line:
            if consecutive_empty_lines_count > CHANGELOG_MAX_EMPTY_LINES:
                if current_version:
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


Markdown.output_formats["plain"] = _unmark_element
# patching Markdown
# noinspection PyTypeChecker
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def _unmark(text):
    return __md.convert(text)

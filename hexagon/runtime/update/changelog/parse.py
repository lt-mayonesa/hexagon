import re
from io import StringIO
from typing import List, Optional

from markdown import Markdown
from packaging.version import parse as parse_version, Version

from hexagon.runtime.update.changelog import ChangelogVersionEntry, ChangelogEntry
from hexagon.runtime.update.changelog.fetch import ChangelogFile

CHANGELOG_MAX_EMPTY_LINES = 10


def parse_changelog(current_hexagon_version: Version, changelog_file: ChangelogFile):
    for line in changelog_file.file.readlines():
        if line.startswith("## v"):
            version = parse_version(line.split(" ")[1])
            if version > current_hexagon_version:
                return _parse_version(version, changelog_file)


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

import re
from io import StringIO

from markdown import Markdown
from packaging.version import parse as parse_version, Version

from hexagon.runtime.update.changelog.fetch import ChangelogFile

CHANGELOG_MAX_EMPTY_LINES = 10


def parse_changelog(current_hexagon_version: Version, changelog_file: ChangelogFile):
    """
    Parse the changelog file and return a simplified view of it.

    The changelog file is expected to be in the following format:
    ```
    ## v0.7.0
    ### Feature
    * feat(task): added something new ()
    * feat(users): added email support ()
    * feat(users): added legs support ()
    ```

    The function will return the following view:
    ```
    ## v0.7.0
    ### tasks
    feat: added something new
    ### users
    feat: added email support
    feat: added legs support
    ```

    """
    changelog = {}
    current_version = None
    for line in changelog_file.readlines():
        if line.startswith("## v"):
            current_version = parse_version(line.split(" ")[1])
            if current_version == current_hexagon_version:
                break
            changelog[current_version] = {}
        else:
            match = re.match(r"^\* (\w+)\((.*)\):\s(.*)\s(\(.*\))", line)
            if match:
                if match.group(2) in changelog[current_version]:
                    changelog[current_version][match.group(2)].append(
                        f"{match.group(1)}: {match.group(3)}"
                    )
                else:
                    changelog[current_version][match.group(2)] = [
                        f"{match.group(1)}: {match.group(3)}"
                    ]

    return "\n".join(
        [
            "\n".join(
                [f"## v{version}"]
                + [
                    "\n".join([f"### {group}"] + entries)
                    for group, entries in entries.items()
                ]
            )
            for version, entries in changelog.items()
        ]
    )


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

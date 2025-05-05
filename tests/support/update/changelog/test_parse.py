from packaging.version import Version

from hexagon.runtime.update.changelog import ChangelogVersionEntry, ChangelogEntry
from hexagon.runtime.update.changelog.fetch import ChangelogFile
from hexagon.runtime.update.changelog.parse import parse_changelog


class MockChangelogFile(ChangelogFile):
    def readlines(self):
        return self.file


def test_parse_empty_changelog_file():
    result = parse_changelog(Version("1.1.1"), MockChangelogFile([]))

    assert result == ""


def test_parse_changelog_file_with_one_version_with_one_feature():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* feat(task): added something new ()",
            ]
        ),
    )

    assert entries == "\n".join(
        [
            "## v0.7.0",
            "### task",
            "feat: added something new",
        ]
    )


def test_parse_changelog_file_with_one_version_with_multiple_features():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* feat(task): added something new ()",
                "* feat(task): added something new 2 ()",
                "* feat(task): added something new 3 ()",
                "* feat(task): added cool stuff ()",
            ]
        ),
    )

    assert entries == "\n".join(
        [
            "## v0.7.0",
            "### task",
            "feat: added something new",
            "feat: added something new 2",
            "feat: added something new 3",
            "feat: added cool stuff",
        ]
    )


def test_parse_changelog_file_with_one_version_with_multiple_features_with_scopes():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* feat(task): added something new ()",
                "* feat(users): added email support ()",
                "* feat(pets): added legs support ()",
            ]
        ),
    )

    assert entries == "\n".join(
        [
            "## v0.7.0",
            "### task",
            "feat: added something new",
            "### users",
            "feat: added email support",
            "### pets",
            "feat: added legs support",
        ]
    )


def test_parse_changelog_file_with_one_version_with_multiple_changes():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* feat(task): added something new ()",
                "### Fix",
                "* fix(bug): fixed something ()",
                "### Documentation",
                "* docs(readme): documented something ()",
            ]
        ),
    )

    assert entries == "\n".join(
        [
            "## v0.7.0",
            "### task",
            "feat: added something new",
            "### bug",
            "fix: fixed something",
            "### readme",
            "docs: documented something",
        ]
    )


def test_parse_changelog_file_with_multiple_new_versions():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* feat(task): added something new ()",
                "## v0.6.9",
                "### Feature",
                "* feat(task): added something ()",
                "* feat(task): added something 2 ()",
                "## v0.5.0",
                "### Fix",
                "* fix(bug): fixed a bug ()",
            ]
        ),
    )

    assert entries == "\n".join(
        [
            "## v0.7.0",
            "### task",
            "feat: added something new",
            "## v0.6.9",
            "### task",
            "feat: added something",
            "feat: added something 2",
            "## v0.5.0",
            "### bug",
            "fix: fixed a bug",
        ]
    )


def test_parse_changelog_file_with_multiple_old_versions():
    entries = parse_changelog(
        Version("1.0.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* feat(task): added something new ()",
                "## v0.6.9",
                "### Feature",
                "* feat(task): added something ()",
                "* feat(task): added something 2 ()",
                "## v0.5.0",
                "### Fix",
                "* fix(bug): fixed a bug ()",
            ]
        ),
    )

    assert entries == "\n".join(
        [
            "## v0.7.0",
            "### task",
            "feat: added something new",
            "## v0.6.9",
            "### task",
            "feat: added something",
            "feat: added something 2",
            "## v0.5.0",
            "### bug",
            "fix: fixed a bug",
        ]
    )


def test_parse_changelog_file_with_old_and_new_versions():
    entries = parse_changelog(
        Version("0.6.9"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* feat(task): added something new ()",
                "## v0.6.9",
                "### Feature",
                "* feat(task): added something ()",
                "* feat(task): added something 2 ()",
                "## v0.5.0",
                "### Fix",
                "* fix(bug): fixed a bug ()",
            ]
        ),
    )

    assert entries == "\n".join(
        [
            "## v0.7.0",
            "### task",
            "feat: added something new",
        ]
    )


def a_changelog_with(lines):
    return MockChangelogFile(
        ["# Changelog", "", "<!--next-version-placeholder-->", "", *lines, ""]
    )

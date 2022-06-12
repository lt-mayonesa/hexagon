from packaging.version import Version

from hexagon.support.update.changelog import ChangelogVersionEntry, ChangelogEntry
from hexagon.support.update.changelog.fetch import ChangelogFile
from hexagon.support.update.changelog.parse import parse_changelog


class MockChangelogFile(ChangelogFile):
    def line(self):
        return self.file.pop(0) if self.file else ""


def test_parse_empty_changelog_file():
    entries = parse_changelog(Version("1.1.1"), MockChangelogFile([]))

    assert entries == []


def test_parse_changelog_file_with_one_version_with_one_feature():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* added something new",
            ]
        ),
    )

    assert entries == [
        a_valid_version_entry("0.7.0", entries=[("Feature", "added something new")])
    ]


def test_parse_changelog_file_with_one_version_with_multiple_features():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* added something new",
                "* added something new 2",
                "* added something new 3",
                "* added cool stuff",
            ]
        ),
    )

    assert entries == [
        a_valid_version_entry(
            "0.7.0",
            entries=[
                ("Feature", "added something new"),
                ("Feature", "added something new 2"),
                ("Feature", "added something new 3"),
                ("Feature", "added cool stuff"),
            ],
        )
    ]


def test_parse_changelog_file_with_one_version_with_multiple_features_with_scopes():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* added something new",
                "* **users** added email support",
                "* **pets** added legs support",
            ]
        ),
    )

    assert entries == [
        a_valid_version_entry(
            "0.7.0",
            entries=[
                ("Feature", "added something new"),
                ("Feature", "users added email support"),
                ("Feature", "pets added legs support"),
            ],
        )
    ]


def test_parse_changelog_file_with_one_version_with_multiple_changes():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* added something new",
                "### Fix",
                "* fixed something",
                "### Documentation",
                "* documented something",
            ]
        ),
    )

    assert entries == [
        a_valid_version_entry(
            "0.7.0",
            entries=[
                ("Feature", "added something new"),
                ("Fix", "fixed something"),
                ("Documentation", "documented something"),
            ],
        )
    ]


def test_parse_changelog_file_with_multiple_new_versions():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* added something new",
                "## v0.6.9",
                "### Feature",
                "* added something",
                "* added something 2",
                "## v0.5.0",
                "### Fix",
                "* fixed a bug",
            ]
        ),
    )

    assert entries == [
        a_valid_version_entry(
            "0.7.0",
            entries=[("Feature", "added something new")],
        ),
        a_valid_version_entry(
            "0.6.9",
            entries=[("Feature", "added something"), ("Feature", "added something 2")],
        ),
        a_valid_version_entry(
            "0.5.0",
            entries=[("Fix", "fixed a bug")],
        ),
    ]


def test_parse_changelog_file_with_multiple_old_versions():
    entries = parse_changelog(
        Version("1.0.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* added something new",
                "## v0.6.9",
                "### Feature",
                "* added something",
                "* added something 2",
                "## v0.5.0",
                "### Fix",
                "* fixed a bug",
            ]
        ),
    )

    assert entries == [
        a_valid_version_entry(
            "0.7.0",
            entries=[("Feature", "added something new")],
        ),
        a_valid_version_entry(
            "0.6.9",
            entries=[("Feature", "added something"), ("Feature", "added something 2")],
        ),
        a_valid_version_entry(
            "0.5.0",
            entries=[("Fix", "fixed a bug")],
        ),
    ]


def test_parse_changelog_file_with_old_and_new_versions():
    entries = parse_changelog(
        Version("0.6.9"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Feature",
                "* added something new",
                "## v0.6.9",
                "### Feature",
                "* added something",
                "* added something 2",
                "## v0.5.0",
                "### Fix",
                "* fixed a bug",
            ]
        ),
    )

    assert entries == [
        a_valid_version_entry(
            "0.7.0",
            entries=[("Feature", "added something new")],
        ),
        a_valid_version_entry("0.6.9"),
    ]


def test_parse_changelog():
    entries = parse_changelog(
        Version("0.1.0"),
        a_changelog_with(
            [
                "## v0.7.0",
                "### Documentation",
                "* Documentation 1",
                "",
                "## v0.6.0",
                "### Fix",
                "* Fix 1",
                "* Fix 2",
                "",
                "## v0.5.0",
                "### Feature",
                "* Feature 1",
                "* Feature 2",
                "",
                "## v0.4.0",
                "### Fix",
                "* Fix 3",
                "### Documentation",
                "* Documentation 2",
                "",
                "## v0.3.0",
                "### Feature",
                "* Feature 3",
                "* Feature 4",
                "### Fix",
                "* Fix 4",
                "### Documentation",
                "* Documentation 3",
                "* Documentation 4",
            ]
        ),
    )

    assert entries == [
        a_valid_version_entry(
            "0.7.0",
            entries=[("Documentation", "Documentation 1")],
        ),
        a_valid_version_entry(
            "0.6.0",
            entries=[("Fix", "Fix 1"), ("Fix", "Fix 2")],
        ),
        a_valid_version_entry(
            "0.5.0",
            entries=[("Feature", "Feature 1"), ("Feature", "Feature 2")],
        ),
        a_valid_version_entry(
            "0.4.0",
            entries=[("Fix", "Fix 3"), ("Documentation", "Documentation 2")],
        ),
        a_valid_version_entry(
            "0.3.0",
            entries=[
                ("Feature", "Feature 3"),
                ("Feature", "Feature 4"),
                ("Fix", "Fix 4"),
                ("Documentation", "Documentation 3"),
                ("Documentation", "Documentation 4"),
            ],
        ),
    ]


def a_changelog_with(lines):
    return MockChangelogFile(
        ["# Changelog", "", "<!--next-version-placeholder-->", "", *lines, ""]
    )


def a_valid_version_entry(version, entries=None):
    entry = ChangelogVersionEntry(version)
    if entries:
        entry.entries = [ChangelogEntry(t, entry) for (t, entry) in entries]
    return entry

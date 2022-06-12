from hexagon.support.update.changelog import ChangelogVersionEntry, ChangelogEntry
from hexagon.support.update.changelog.format import format_entries


def test_format_empty_entries_list():
    entries = format_entries([])

    assert entries == []


def test_format_one_version_with_single_entry():
    entries = format_entries(
        [a_valid_version_entry("0.1.0", entries=[("Feature", "added something")])]
    )

    assert entries == [ChangelogEntry("Feature", "added something")]


def test_format_one_version_with_multiple_feature_entries():
    entries = format_entries(
        [
            a_valid_version_entry(
                "0.1.0",
                entries=[
                    ("Feature", "added something 1"),
                    ("Feature", "added something 2"),
                    ("Feature", "added something 3"),
                ],
            )
        ]
    )

    assert entries == [
        ChangelogEntry("Feature", "added something 1"),
        ChangelogEntry("Feature", "added something 2"),
        ChangelogEntry("Feature", "added something 3"),
    ]


def test_format_one_version_with_multiple_type_entries():
    entries = format_entries(
        [
            a_valid_version_entry(
                "0.1.0",
                entries=[
                    ("Fix", "fixed something 1"),
                    ("Feature", "added something 2"),
                    ("Documentation", "documented something 3"),
                ],
            )
        ]
    )

    assert entries == [
        ChangelogEntry("Feature", "added something 2"),
        ChangelogEntry("Fix", "fixed something 1"),
        ChangelogEntry("Documentation", "documented something 3"),
    ]


def test_format_many_versions_with_multiple_type_entries():
    entries = format_entries(
        [
            a_valid_version_entry(
                "0.3.0",
                entries=[
                    ("Fix", "fixed something 1"),
                    ("Feature", "added something 2"),
                    ("Documentation", "documented something 3"),
                ],
            ),
            a_valid_version_entry(
                "0.2.0",
                entries=[
                    ("Feature", "added something 2.3"),
                ],
            ),
            a_valid_version_entry(
                "0.1.0",
                entries=[
                    ("Fix", "fixed something 1.2"),
                    ("Documentation", "documented something 3.4"),
                ],
            ),
        ]
    )

    assert entries == [
        ChangelogEntry("Feature", "added something 2"),
        ChangelogEntry("Feature", "added something 2.3"),
        ChangelogEntry("Fix", "fixed something 1"),
        ChangelogEntry("Fix", "fixed something 1.2"),
        ChangelogEntry("Documentation", "documented something 3"),
        ChangelogEntry("Documentation", "documented something 3.4"),
    ]


def a_valid_version_entry(version, entries=None):
    entry = ChangelogVersionEntry(version)
    if entries:
        entry.entries = [ChangelogEntry(t, entry) for (t, entry) in entries]
    return entry

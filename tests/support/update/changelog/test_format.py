from hexagon.runtime.update.changelog import ChangelogVersionEntry, ChangelogEntry
from hexagon.runtime.update.changelog.format import format_entries


def test_format_entries_returns_empty_list_when_given_empty_list():
    """
    Given an empty list of changelog version entries.
    When format_entries is called with this empty list.
    Then an empty list should be returned.
    """
    entries = format_entries([])

    assert entries == []


def test_format_entries_returns_single_changelog_entry_when_given_one_version_with_one_entry():
    """
    Given a list with one ChangelogVersionEntry for version '0.1.0' containing one feature entry.
    When format_entries is called with this list.
    Then a list with a single ChangelogEntry should be returned.
    And the entry should have type 'Feature' and content 'added something'.
    """
    entries = format_entries(
        [a_valid_version_entry("0.1.0", entries=[("Feature", "added something")])]
    )

    assert entries == [ChangelogEntry("Feature", "added something")]


def test_format_entries_preserves_order_of_entries_when_given_one_version_with_multiple_feature_entries():
    """
    Given a list with one ChangelogVersionEntry for version '0.1.0' containing three feature entries.
    When format_entries is called with this list.
    Then a list with three ChangelogEntry objects should be returned.
    And the entries should maintain their original order with types 'Feature' and respective content.
    """
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


def test_format_entries_sorts_entries_by_type_when_given_one_version_with_different_entry_types():
    """
    Given a list with one ChangelogVersionEntry for version '0.1.0' containing entries of different types.
    When format_entries is called with this list.
    Then a list of ChangelogEntry objects should be returned.
    And the entries should be ordered by type (Feature, Fix, Documentation) regardless of original order.
    """
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


def test_format_entries_groups_and_sorts_entries_by_type_across_multiple_versions():
    """
    Given a list with three ChangelogVersionEntry objects for versions '0.3.0', '0.2.0', and '0.1.0'.
    And each version contains entries of different types.
    When format_entries is called with this list.
    Then a list of ChangelogEntry objects should be returned.
    And the entries should be grouped by type (Feature, Fix, Documentation) across all versions.
    And within each type group, entries should be ordered by their original version order.
    """
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

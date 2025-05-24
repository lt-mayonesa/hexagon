from packaging.version import Version

from hexagon.runtime.update.changelog.fetch import ChangelogFile
from hexagon.runtime.update.changelog.parse import parse_changelog


class MockChangelogFile(ChangelogFile):
    def readlines(self):
        return self.file


def test_parse_changelog_returns_empty_string_for_empty_file():
    """
    Given an empty changelog file (empty list of lines).
    When parse_changelog is called with version='1.1.1' and this empty file.
    Then an empty string should be returned.
    """
    result = parse_changelog(Version("1.1.1"), MockChangelogFile([]))

    assert result == ""


def test_parse_changelog_formats_single_feature_entry_correctly():
    """
    Given a changelog file with version 'v0.7.0' containing one feature entry 'feat(task): added something new ()'.
    When parse_changelog is called with version='0.1.0' and this changelog.
    Then the returned string should contain the version header 'v0.7.0'.
    And a scope header '### task'.
    And the formatted feature entry 'feat: added something new'.
    """
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


def test_parse_changelog_formats_multiple_features_with_same_scope_correctly():
    """
    Given a changelog file with version 'v0.7.0' containing multiple feature entries with the same 'task' scope.
    When parse_changelog is called with version='0.1.0' and this changelog.
    Then the returned string should contain the version header 'v0.7.0'.
    And a single scope header '### task'.
    And all feature entries should be listed under that scope with their descriptions.
    """
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


def test_parse_changelog_groups_features_by_scope_with_separate_headers():
    """
    Given a changelog file with version 'v0.7.0' containing features with different scopes ('task', 'users', 'pets').
    When parse_changelog is called with version='0.1.0' and this changelog.
    Then the returned string should contain the version header 'v0.7.0'.
    And separate scope headers for each scope ('### task', '### users', '### pets').
    And features should be grouped under their respective scope headers.
    """
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


def test_parse_changelog_formats_different_change_types_correctly():
    """
    Given a changelog file with version 'v0.7.0' containing different types of changes (feature, fix, documentation).
    When parse_changelog is called with version='0.1.0' and this changelog.
    Then the returned string should contain the version header 'v0.7.0'.
    And separate scope headers for each scope ('task', 'bug', 'readme').
    And each change type should be formatted with its type prefix ('feat:', 'fix:', 'docs:') under the appropriate scope.
    """
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


def test_parse_changelog_includes_all_versions_when_current_version_is_older():
    """
    Given a changelog file with multiple versions ('v0.7.0', 'v0.6.9', 'v0.5.0') all newer than current version '0.1.0'.
    When parse_changelog is called with version='0.1.0' and this changelog.
    Then the returned string should include all version headers ('v0.7.0', 'v0.6.9', 'v0.5.0').
    And all changes from each version should be included in the result with appropriate formatting.
    """
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


def test_parse_changelog_includes_all_versions_when_current_version_is_newer():
    """
    Given a changelog file with multiple versions ('v0.7.0', 'v0.6.9', 'v0.5.0') all older than current version '1.0.0'.
    When parse_changelog is called with version='1.0.0' and this changelog.
    Then the returned string should include all version headers ('v0.7.0', 'v0.6.9', 'v0.5.0').
    And all changes from each version should be included in the result with appropriate formatting.
    """
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


def test_parse_changelog_includes_only_newer_versions_when_mixed_versions_exist():
    """
    Given a changelog file with versions 'v0.7.0', 'v0.6.9', and 'v0.5.0'.
    When parse_changelog is called with current version='0.6.9'.
    Then only the version newer than current ('v0.7.0') should be included in the result.
    And older versions ('v0.6.9', 'v0.5.0') should be excluded from the result.
    """
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

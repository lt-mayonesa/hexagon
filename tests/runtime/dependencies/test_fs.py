import os
import tempfile
from pathlib import PosixPath

import pytest

from hexagon.runtime.dependencies.fs import declarations_found


def test_declarations_found_returns_empty_list_when_directory_is_empty():
    """
    Given an empty temporary directory
    When declarations_found is called with file names ['requirements.txt', 'Pipfile']
    Then an empty list should be returned
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        assert declarations_found(tmpdir, ["requirements.txt"]) == []
        assert declarations_found(tmpdir, ["Pipfile"]) == []
        assert declarations_found(tmpdir, ["requirements.txt", "Pipfile"]) == []


@pytest.mark.parametrize(
    "dependency_file",
    [
        "requirements.txt",
        "Pipfile",
    ],
)
def test_declarations_found_returns_single_entry_when_one_dependency_file_exists(
    dependency_file,
):
    """
    Given a temporary directory containing a single dependency file (requirements.txt or Pipfile).
    When declarations_found is called with that file name.
    Then a list with one tuple should be returned.
    And the tuple should contain the directory path and a list with the dependency file name.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, dependency_file), "w") as f:
            f.write("test")

        assert declarations_found(tmpdir, [dependency_file]) == [
            (
                PosixPath(tmpdir),
                [dependency_file],
            ),
        ]


def test_declarations_found_returns_single_entry_with_multiple_files_when_multiple_dependency_files_exist_in_same_directory():
    """
    Given a temporary directory containing both 'requirements.txt' and 'Pipfile'.
    When declarations_found is called with both file names.
    Then a list with one tuple should be returned.
    And the tuple should contain the directory path and a list with both dependency file names.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "requirements.txt"), "w") as f:
            f.write("test")

        with open(os.path.join(tmpdir, "Pipfile"), "w") as f:
            f.write("test")

        assert declarations_found(tmpdir, ["requirements.txt", "Pipfile"]) == [
            (
                PosixPath(tmpdir),
                ["requirements.txt", "Pipfile"],
            ),
        ]


def test_declarations_found_returns_multiple_entries_when_dependency_files_exist_in_parent_and_child_directories():
    """
    Given a temporary directory and a subdirectory, both containing 'requirements.txt' and 'Pipfile'.
    When declarations_found is called with both file names on the parent directory.
    Then a list with two tuples should be returned.
    And the first tuple should contain the parent directory path and both dependency file names.
    And the second tuple should contain the subdirectory path and both dependency file names.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "requirements.txt"), "w") as f:
            f.write("test")

        with open(os.path.join(tmpdir, "Pipfile"), "w") as f:
            f.write("test")

        subdir = os.path.join(tmpdir, "subdir")
        os.makedirs(subdir, exist_ok=True)

        with open(os.path.join(subdir, "requirements.txt"), "w") as f:
            f.write("test")

        with open(os.path.join(subdir, "Pipfile"), "w") as f:
            f.write("test")

        assert declarations_found(tmpdir, ["requirements.txt", "Pipfile"]) == [
            (
                PosixPath(tmpdir),
                ["requirements.txt", "Pipfile"],
            ),
            (
                PosixPath(subdir),
                ["requirements.txt", "Pipfile"],
            ),
        ]


def test_declarations_found_returns_entries_for_all_directories_with_dependency_files_recursively():
    """
    Given a directory structure with:
      - A root directory containing 'requirements.txt' and 'Pipfile'
      - A subdirectory containing 'requirements.txt' and 'Pipfile'
      - A sub-subdirectory containing 'requirements.txt' and 'Pipfile'
      - Another subdirectory containing only 'Pipfile'
    When declarations_found is called with both file names on the root directory.
    Then a list with four tuples should be returned.
    And each tuple should contain the corresponding directory path and the dependency files found in that directory.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "requirements.txt"), "w") as f:
            f.write("test")

        with open(os.path.join(tmpdir, "Pipfile"), "w") as f:
            f.write("test")

        subdir = os.path.join(tmpdir, "subdir")
        os.makedirs(subdir, exist_ok=True)

        with open(os.path.join(subdir, "requirements.txt"), "w") as f:
            f.write("test")

        with open(os.path.join(subdir, "Pipfile"), "w") as f:
            f.write("test")

        sub_subdir = os.path.join(subdir, "sub_subdir")
        os.makedirs(sub_subdir, exist_ok=True)

        with open(os.path.join(sub_subdir, "requirements.txt"), "w") as f:
            f.write("test")

        with open(os.path.join(sub_subdir, "Pipfile"), "w") as f:
            f.write("test")

        another_subdir = os.path.join(tmpdir, "another_subdir")
        os.makedirs(another_subdir, exist_ok=True)

        with open(os.path.join(another_subdir, "Pipfile"), "w") as f:
            f.write("test")

        assert declarations_found(tmpdir, ["requirements.txt", "Pipfile"]) == [
            (
                PosixPath(tmpdir),
                ["requirements.txt", "Pipfile"],
            ),
            (
                PosixPath(subdir),
                ["requirements.txt", "Pipfile"],
            ),
            (
                PosixPath(sub_subdir),
                ["requirements.txt", "Pipfile"],
            ),
            (
                PosixPath(another_subdir),
                ["Pipfile"],
            ),
        ]

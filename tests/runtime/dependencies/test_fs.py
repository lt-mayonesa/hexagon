import os
import tempfile
from pathlib import PosixPath

import pytest

from hexagon.runtime.dependencies.fs import declarations_found


def test_no_declarations_found():
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
def test_find_declaration_in_single_level_directory(dependency_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, dependency_file), "w") as f:
            f.write("test")

        assert declarations_found(tmpdir, [dependency_file]) == [
            (
                PosixPath(tmpdir),
                [dependency_file],
            ),
        ]


def test_find_multiple_declarations_in_same_directory():
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


def test_find_declaration_in_sub_directories():
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


def test_find_declaration_recursively_in_directories():
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

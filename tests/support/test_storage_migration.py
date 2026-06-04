import importlib
import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

import hexagon
from hexagon.domain.cli import Cli

storage_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), ".storage-migration")
)


@pytest.fixture(autouse=True)
def reset_storage():
    importlib.reload(hexagon.support.storage)
    os.environ["HEXAGON_STORAGE_PATH"] = storage_path
    if os.path.exists(storage_path):
        shutil.rmtree(storage_path)
    Path(storage_path).mkdir(exist_ok=True, parents=True)


def _make_cli(name: str, command: str) -> Cli:
    return Cli(name=name, command=command)


def _create_storage_dir(key: str, files: dict = None):
    """Create a storage directory with optional files."""
    dir_path = os.path.join(storage_path, key)
    Path(dir_path).mkdir(exist_ok=True, parents=True)
    for filename, content in (files or {}).items():
        with open(os.path.join(dir_path, filename), "w") as f:
            f.write(content)
    return dir_path


def test_migrate_storage_to_command_key_renames_old_dir_to_command_key():
    """
    Given only an old storage directory named after cli.name.lower() exists.
    When migrate_storage_to_command_key is called.
    Then the old directory should be renamed to cli.command.
    And all files should be accessible under the new path.
    """
    from hexagon.support.storage.migration import migrate_storage_to_command_key

    cli = _make_cli("My Team CLI", "my-team")
    _create_storage_dir("my team cli", {"last-command.txt": "my-team tool env"})

    migrate_storage_to_command_key(cli)

    assert not os.path.exists(os.path.join(storage_path, "my team cli"))
    assert os.path.isdir(os.path.join(storage_path, "my-team"))
    with open(os.path.join(storage_path, "my-team", "last-command.txt")) as f:
        assert f.read() == "my-team tool env"


def test_migrate_storage_to_command_key_does_nothing_when_no_old_dir_exists():
    """
    Given no storage directory exists for this CLI.
    When migrate_storage_to_command_key is called.
    Then no directory should be created and no error should be raised.
    """
    from hexagon.support.storage.migration import migrate_storage_to_command_key

    cli = _make_cli("My Team CLI", "my-team")

    migrate_storage_to_command_key(cli)

    assert not os.path.exists(os.path.join(storage_path, "my team cli"))
    assert not os.path.exists(os.path.join(storage_path, "my-team"))


def test_migrate_storage_to_command_key_does_nothing_when_only_new_dir_exists():
    """
    Given only a storage directory named after cli.command already exists.
    When migrate_storage_to_command_key is called.
    Then the directory should remain untouched and no error should be raised.
    """
    from hexagon.support.storage.migration import migrate_storage_to_command_key

    cli = _make_cli("My Team CLI", "my-team")
    _create_storage_dir("my-team", {"last-command.txt": "existing"})

    migrate_storage_to_command_key(cli)

    assert os.path.isdir(os.path.join(storage_path, "my-team"))
    assert not os.path.exists(os.path.join(storage_path, "my team cli"))
    with open(os.path.join(storage_path, "my-team", "last-command.txt")) as f:
        assert f.read() == "existing"


def test_migrate_storage_to_command_key_does_nothing_when_name_equals_command():
    """
    Given a CLI whose name.lower() already equals its command.
    When migrate_storage_to_command_key is called.
    Then no rename should occur and the directory remains as-is.
    """
    from hexagon.support.storage.migration import migrate_storage_to_command_key

    cli = _make_cli("pmp", "pmp")
    _create_storage_dir("pmp", {"last-command.txt": "pmp tool env"})

    migrate_storage_to_command_key(cli)

    assert os.path.isdir(os.path.join(storage_path, "pmp"))
    with open(os.path.join(storage_path, "pmp", "last-command.txt")) as f:
        assert f.read() == "pmp tool env"


def test_migrate_storage_to_command_key_shows_warning_when_both_dirs_exist():
    """
    Given both the old (cli.name.lower()) and new (cli.command) storage directories exist.
    When migrate_storage_to_command_key is called.
    Then neither directory should be modified.
    And a warning panel should be shown to the user.
    """
    from hexagon.support.storage.migration import migrate_storage_to_command_key

    cli = _make_cli("My Team CLI", "my-team")
    _create_storage_dir("my team cli", {"old-data.txt": "old"})
    _create_storage_dir("my-team", {"new-data.txt": "new"})

    with patch("hexagon.support.output.printer.log") as mock_log:
        migrate_storage_to_command_key(cli)

    assert os.path.isdir(os.path.join(storage_path, "my team cli"))
    assert os.path.isdir(os.path.join(storage_path, "my-team"))
    mock_log.panel.assert_called_once()


def test_migrate_storage_to_command_key_does_not_warn_on_clean_migration():
    """
    Given only the old storage directory exists.
    When migrate_storage_to_command_key is called and succeeds.
    Then no warning should be shown to the user.
    """
    from hexagon.support.storage.migration import migrate_storage_to_command_key

    cli = _make_cli("My Team CLI", "my-team")
    _create_storage_dir("my team cli", {"last-command.txt": "data"})

    with patch("hexagon.support.output.printer.log") as mock_log:
        migrate_storage_to_command_key(cli)

    mock_log.panel.assert_not_called()

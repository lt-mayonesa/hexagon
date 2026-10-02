import os
import shutil
from pathlib import Path

import pytest

from hexagon.support.config_file.manager import ConfigFileManager

_TEST_DIR = os.path.realpath(
    os.path.join(os.path.dirname(__file__), ".config-file-manager")
)


@pytest.fixture(autouse=True)
def clean_test_dir():
    if os.path.exists(_TEST_DIR):
        shutil.rmtree(_TEST_DIR)
    Path(_TEST_DIR).mkdir(exist_ok=True, parents=True)
    yield
    if os.path.exists(_TEST_DIR):
        shutil.rmtree(_TEST_DIR)


def _file_path(name: str = "test.yml") -> str:
    return os.path.join(_TEST_DIR, name)


def test_exists_returns_false_when_file_missing():
    """
    Given a path that does not exist on disk.
    When exists is checked.
    Then it returns False.
    """
    mgr = ConfigFileManager(_file_path("missing.yml"))
    assert not mgr.exists


def test_exists_returns_true_when_file_present():
    """
    Given a file that has been created on disk.
    When exists is checked.
    Then it returns True.
    """
    path = _file_path()
    Path(path).write_text("key: value\n")
    mgr = ConfigFileManager(path)
    assert mgr.exists


def test_load_returns_none_when_file_missing():
    """
    Given a path with no file.
    When load is called.
    Then it returns None.
    """
    mgr = ConfigFileManager(_file_path("missing.yml"))
    assert mgr.load() is None


def test_load_returns_dict_contents():
    """
    Given a YAML file with key-value pairs.
    When load is called.
    Then the contents are returned as a plain dict.
    """
    path = _file_path()
    Path(path).write_text("theme: dark\nupdate_disabled: true\n")
    mgr = ConfigFileManager(path)
    result = mgr.load()
    assert result == {"theme": "dark", "update_disabled": True}


def test_load_returns_empty_dict_for_empty_file():
    """
    Given an empty YAML file.
    When load is called.
    Then an empty dict is returned.
    """
    path = _file_path()
    Path(path).write_text("")
    mgr = ConfigFileManager(path)
    assert mgr.load() == {}


def test_set_value_updates_in_memory_content():
    """
    Given a loaded manager.
    When set_value is called.
    Then the key is updated in memory (not yet persisted).
    """
    path = _file_path()
    Path(path).write_text("theme: default\n")
    mgr = ConfigFileManager(path)
    mgr.load()
    mgr.set_value("theme", "dark")
    assert mgr._content["theme"] == "dark"


def test_set_value_auto_loads_when_content_is_none():
    """
    Given a file on disk and a manager that hasn't called load.
    When set_value is called.
    Then it loads the file automatically and applies the change.
    """
    path = _file_path()
    Path(path).write_text("theme: default\n")
    mgr = ConfigFileManager(path)
    mgr.set_value("theme", "dark")
    assert mgr._content["theme"] == "dark"


def test_save_persists_changes_to_disk():
    """
    Given set_value has been called.
    When save is called.
    Then the file on disk reflects the updated value.
    """
    path = _file_path()
    Path(path).write_text("theme: default\n")
    mgr = ConfigFileManager(path)
    mgr.load()
    mgr.set_value("theme", "dark")
    mgr.save()

    mgr2 = ConfigFileManager(path)
    assert mgr2.load() == {"theme": "dark"}


def test_create_writes_empty_file_when_no_initial_content():
    """
    Given a path that does not exist.
    When create is called with no arguments.
    Then an empty YAML file is created.
    """
    path = _file_path("new.yml")
    mgr = ConfigFileManager(path)
    mgr.create()
    assert mgr.exists
    assert mgr.load() == {}


def test_create_writes_initial_content_to_file():
    """
    Given a path that does not exist.
    When create is called with initial_content.
    Then the file is created with that content.
    """
    path = _file_path("new.yml")
    mgr = ConfigFileManager(path)
    mgr.create({"theme": "dark", "hints_disabled": True})
    assert mgr.load() == {"theme": "dark", "hints_disabled": True}


def test_unset_value_removes_key_and_returns_true():
    """
    Given a file with a key.
    When unset_value is called with that key.
    Then the key is removed and True is returned.
    """
    path = _file_path()
    Path(path).write_text("theme: dark\nupdate_disabled: true\n")
    mgr = ConfigFileManager(path)
    mgr.load()
    result = mgr.unset_value("theme")
    assert result is True
    assert "theme" not in mgr._content


def test_unset_value_returns_false_when_key_not_present():
    """
    Given a file without the target key.
    When unset_value is called.
    Then False is returned and content is unchanged.
    """
    path = _file_path()
    Path(path).write_text("update_disabled: true\n")
    mgr = ConfigFileManager(path)
    mgr.load()
    result = mgr.unset_value("nonexistent_key")
    assert result is False


def test_get_returns_value_for_existing_key():
    """
    Given a loaded file with a key.
    When get is called with that key.
    Then the value is returned.
    """
    path = _file_path()
    Path(path).write_text("theme: dark\n")
    mgr = ConfigFileManager(path)
    mgr.load()
    assert mgr.get("theme") == "dark"


def test_get_returns_default_for_missing_key():
    """
    Given a loaded file without the target key.
    When get is called with a default.
    Then the default is returned.
    """
    path = _file_path()
    Path(path).write_text("theme: dark\n")
    mgr = ConfigFileManager(path)
    mgr.load()
    assert mgr.get("missing", "fallback") == "fallback"

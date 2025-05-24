import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from ruamel.yaml import YAML

import hexagon
from hexagon.support.storage import (
    store_user_data,
    load_user_data,
)

storage_path = os.path.realpath(os.path.join(os.path.dirname(__file__), ".storage"))

app = "test"
key = "data"


@pytest.fixture(autouse=True)
def set_storage_path():
    # reload storage module
    import importlib

    importlib.reload(hexagon.support.storage)

    os.environ["HEXAGON_STORAGE_PATH"] = storage_path
    if os.path.exists(storage_path):
        shutil.rmtree(storage_path)
    Path(storage_path).mkdir(exist_ok=True, parents=True)


def _create_dir_for_file(file_path: str):
    Path(os.path.dirname(file_path)).mkdir(exist_ok=True, parents=True)


def test_store_user_data_saves_single_line_text_to_file():
    """
    Given a single line text 'text-single-line'.
    When storing it as user data with key='data' and app='test'.
    Then it should be saved to a .txt file at the path '[storage_path]/test/data.txt'.
    And the file content should exactly match the input text.
    """
    text = "text-single-line"
    store_user_data(key, text, app=app)

    with open(os.path.join(storage_path, app, key) + ".txt", "r") as file:
        assert file.read() == text


def test_store_user_data_appends_text_to_existing_file_when_append_is_true():
    """
    Given an existing file at '[storage_path]/test/data.txt' with content 'appended:'.
    When storing text 'text' with args append=True, key='data', and app='test'.
    Then the text should be appended to the existing content.
    And the final file content should be 'appended: text'.
    """
    file_path = os.path.join(storage_path, app, key) + ".txt"
    _create_dir_for_file(file_path)
    with open(file_path, "w") as file:
        file.write("appended: ")

    store_user_data(key, "text", append=True, app=app)

    with open(file_path, "r") as file:
        assert file.read() == "appended: text"


def test_store_user_data_saves_multiline_text_to_file():
    """
    Given a list of text lines ['text', 'multi', 'line'].
    When storing it as user data with key='data' and app='test'.
    Then the lines should be saved to a .txt file at the path '[storage_path]/test/data.txt'.
    And each line in the file should match the corresponding input line.
    """
    text = ["text", "multi", "line"]
    store_user_data(key, text, app=app)

    with open(os.path.join(storage_path, app, key) + ".txt", "r") as file:
        assert list(line.rstrip() for line in file.readlines()) == text


def test_store_user_data_appends_multiline_text_to_existing_file_when_append_is_true():
    """
    Given an existing file at '[storage_path]/test/data.txt' with 3 lines of content 'existing line 1-3'.
    When storing a list of text lines ['added line 4', 'added line 5', 'added line 6'] with append=True.
    Then the new lines should be appended after the existing content.
    And the final file should contain all 6 lines in the correct order.
    """
    file_path = os.path.join(storage_path, app, key) + ".txt"
    _create_dir_for_file(file_path)
    existing_lines = list(f"existing line {i}\n" for i in range(1, 4))
    with open(file_path, "w") as file:
        file.writelines(existing_lines)

    existing_lines = list(line.rstrip() for line in existing_lines)
    added_lines = list(f"added line {i}" for i in range(4, 7))

    store_user_data(key, added_lines, append=True, app=app)

    with open(file_path, "r") as file:
        assert (
            list(line.rstrip() for line in file.readlines())
            == existing_lines + added_lines
        )


def test_store_user_data_saves_dictionary_to_yaml_file():
    """
    Given a dictionary with nested structure containing properties and a nested dictionary.
    When storing it as user data with key='data' and app='test'.
    Then it should be saved as YAML to the file path '[storage_path]/test/data.yaml'.
    And the loaded YAML content should exactly match the input dictionary.
    """
    dictionary = {
        "prop1": 1,
        "prop2": 123,
        "nested": {"nested1": "n1", "nested2": "n123"},
    }

    store_user_data(key, dictionary, app=app)

    with open(os.path.join(storage_path, app, key) + ".yaml", "r") as file:
        assert YAML().load(file) == dictionary


def test_store_user_data_merges_dictionary_with_existing_yaml_when_append_is_true():
    """
    Given an existing YAML file at '[storage_path]/test/data.yaml' with a dictionary containing properties and nested objects.
    When storing a new dictionary with some overlapping keys and new keys with append=True.
    Then the dictionaries should be merged with new values overriding existing ones for the same keys.
    And nested dictionaries should be recursively merged preserving non-overlapping keys.
    And the result should be saved back to the same YAML file.
    """
    file_path, existing_dictionary = _given_an_existing_dictionary(
        {
            "prop1": 1,
            "prop2": 123,
            "nested": {"nested1": "n1", "nested2": "n123"},
        }
    )

    added_dictionary = {
        "newProp": "new",
        "prop2": 12345,
        "nested": {"nested2": "n12345", "newNested": "newNested"},
    }

    store_user_data(key, added_dictionary, append=True, app=app)

    with open(file_path, "r") as file:
        assert YAML().load(file) == {
            "prop1": 1,
            "prop2": 12345,
            "newProp": "new",
            "nested": {"nested1": "n1", "nested2": "n12345", "newNested": "newNested"},
        }


def _given_an_existing_dictionary(values):
    file_path = os.path.join(storage_path, app, key) + ".yaml"
    _create_dir_for_file(file_path)
    existing_dictionary = values
    with open(file_path, "w") as file:
        YAML().dump(existing_dictionary, file)
    return file_path, existing_dictionary


def test_store_user_data_creates_nested_directory_structure_for_nested_keys():
    """
    Given a key 'very.nested.key' with dots representing directory hierarchy.
    When storing text 'text-single-line' with this key and app='test'.
    Then the data should be saved at the path '[storage_path]/test/very/nested/key.txt'.
    And the file content should match the input text.
    """
    text = "text-single-line"
    store_user_data("very.nested.key", text, app=app)

    with open(
        os.path.join(storage_path, app, "very", "nested", "key") + ".txt", "r"
    ) as file:
        assert file.read() == text


def test_load_user_data_returns_text_from_existing_file():
    """
    Given an existing text file at '[storage_path]/test/data.txt' with content 'existing text'.
    When calling load_user_data with key='data' and app='test'.
    Then the exact content of the file 'existing text' should be returned as a string.
    """
    text = "existing text"
    file_path = os.path.join(storage_path, app, key) + ".txt"
    _create_dir_for_file(file_path)
    with open(file_path, "w") as file:
        file.write(text)

    assert load_user_data(key, app=app) == text


def test_load_user_data_returns_lines_from_existing_multiline_file():
    """
    Given an existing text file at '[storage_path]/test/data.txt' with 3 lines of content.
    When calling load_user_data with key='data' and app='test'.
    Then the content should be returned as a list containing the 3 lines from the file.
    """
    file_path = os.path.join(storage_path, app, key) + ".txt"
    _create_dir_for_file(file_path)
    existing_lines = list(f"existing line {i}\n" for i in range(1, 4))
    with open(file_path, "w") as file:
        file.writelines(existing_lines)

    assert load_user_data(key, app=app) == existing_lines


def test_load_user_data_returns_dictionary_from_existing_yaml_file():
    """
    Given an existing YAML file at '[storage_path]/test/data.yaml' with a nested dictionary structure.
    When calling load_user_data with key='data' and app='test'.
    Then the content should be returned as a Python dictionary matching the structure in the YAML file.
    """
    file_path, existing_dictionary = _given_an_existing_dictionary(
        {
            "prop1": 1,
            "prop2": 123,
            "nested": {"nested1": "n1", "nested2": "n123"},
        }
    )

    assert load_user_data(key, app=app) == existing_dictionary


def test_store_user_data_uses_hexagon_as_default_app_when_not_specified():
    """
    Given no app parameter is specified when calling store_user_data.
    When storing string 'data' with key='data'.
    Then the data should be saved to the file '[storage_path]/hexagon/data.txt'.
    And the file content should match the input string.
    """
    store_user_data(key, "data")

    with open(os.path.join(storage_path, "hexagon", key) + ".txt") as file:
        assert file.read() == "data"


@patch("hexagon.runtime.configuration.Configuration.has_config", True)
def test_store_user_data_uses_configured_app_name_when_available():
    """
    Given the CLI has a configured name 'test-app' and Configuration.has_config is True.
    When storing string 'data' with key='data' and no app parameter.
    Then the data should be saved to the file '[storage_path]/test-app/data.txt'.
    And the file content should match the input string.
    """
    from hexagon.runtime.singletons import cli

    cli.name = "test-app"

    store_user_data(key, "data")

    with open(os.path.join(storage_path, "test-app", key) + ".txt") as file:
        assert file.read() == "data"

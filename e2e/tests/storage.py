import pytest
from unittest.mock import patch
import os
import shutil
from pathlib import Path
from ruamel.yaml import YAML

from hexagon.support.storage import store_user_data, load_user_data
from hexagon.cli import cli

storage_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, "storage")
)

app = "test"
key = "data"


@pytest.fixture(autouse=True)
def set_storage_path():
    os.environ["HEXAGON_STORAGE_PATH"] = storage_path
    if os.path.exists(storage_path):
        shutil.rmtree(storage_path)
    Path(storage_path).mkdir(exist_ok=True, parents=True)


def _create_dir_for_file(file_path: str):
    Path(os.path.dirname(file_path)).mkdir(exist_ok=True, parents=True)


def test_storage_text():
    text = "text-single-line"
    store_user_data(key, text, app=app)

    with open(os.path.join(storage_path, app, key) + ".txt", "r") as file:
        assert file.read() == text


def test_storage_text_append():
    file_path = os.path.join(storage_path, app, key) + ".txt"
    _create_dir_for_file(file_path)
    with open(file_path, "w") as file:
        file.write("appended: ")

    store_user_data(key, "text", append=True, app=app)

    with open(file_path, "r") as file:
        assert file.read() == "appended: text"


def test_storage_text_multiline():
    text = ["text", "multi", "line"]
    store_user_data(key, text, app=app)

    with open(os.path.join(storage_path, app, key) + ".txt", "r") as file:
        assert list(line.rstrip() for line in file.readlines()) == text


def test_storage_text_multiline_append():
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


def test_storage_dictionary():
    dictionary = {
        "prop1": 1,
        "prop2": 123,
        "nested": {"nested1": "n1", "nested2": "n123"},
    }

    store_user_data(key, dictionary, app=app)

    with open(os.path.join(storage_path, app, key) + ".yaml", "r") as file:
        assert YAML().load(file) == dictionary


def test_storage_dictionary_append():
    file_path = os.path.join(storage_path, app, key) + ".yaml"
    _create_dir_for_file(file_path)
    existing_dictionary = {
        "prop1": 1,
        "prop2": 123,
        "nested": {"nested1": "n1", "nested2": "n123"},
    }

    with open(file_path, "w") as file:
        YAML().dump(existing_dictionary, file)

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


def test_storage_nested_key():
    text = "text-single-line"
    store_user_data("very.nested.key", text, app=app)

    with open(
        os.path.join(storage_path, app, "very", "nested", "key") + ".txt", "r"
    ) as file:
        assert file.read() == text


def test_storage_load_existing_text():
    text = "existing text"
    file_path = os.path.join(storage_path, app, key) + ".txt"
    _create_dir_for_file(file_path)
    with open(file_path, "w") as file:
        file.write(text)

    assert load_user_data(key, app=app) == text


def test_storage_load_existing_text_multiline():
    file_path = os.path.join(storage_path, app, key) + ".txt"
    _create_dir_for_file(file_path)
    existing_lines = list(f"existing line {i}\n" for i in range(1, 4))
    with open(file_path, "w") as file:
        file.writelines(existing_lines)

    assert load_user_data(key, app=app) == existing_lines


def test_storage_load_existing_dictionary():
    file_path = os.path.join(storage_path, app, key) + ".yaml"
    _create_dir_for_file(file_path)
    existing_dictionary = {
        "prop1": 1,
        "prop2": 123,
        "nested": {"nested1": "n1", "nested2": "n123"},
    }

    with open(file_path, "w") as file:
        YAML().dump(existing_dictionary, file)

    assert load_user_data(key, app=app) == existing_dictionary


def test_storage_default_app():
    store_user_data(key, "data")

    with open(os.path.join(storage_path, "hexagon", key) + ".txt") as file:
        assert file.read() == "data"


@patch("hexagon.cli.configuration.has_config", True)
def test_storage_configured_app():
    cli["name"] = "test-app"
    store_user_data(key, "data")

    with open(os.path.join(storage_path, "test-app", key) + ".txt") as file:
        assert file.read() == "data"

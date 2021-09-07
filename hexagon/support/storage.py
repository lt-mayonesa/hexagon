from hexagon.utils.dict import merge_dictionaries_deep
import os
from pathlib import Path
import sys
from typing import Any, Dict, List
from ruamel.yaml import YAML
from enum import Enum
from shutil import rmtree

HEXAGON_STORAGE_APP = "hexagon"


class HexagonStorageKeys(Enum):
    options = "options"
    last_command = "last-command"
    last_update_check = "last-update-check"


class StorageValueType(Enum):
    text = "text"
    text_multiline = "text-multilne"
    dictionary = "dictionary"


class StoragePurpose(Enum):
    config = "config"
    data = "local/share"


_extension_by_value_type = {
    StorageValueType.text: ".txt",
    StorageValueType.text_multiline: ".txt",
    StorageValueType.dictionary: ".yaml",
}


_config_storage_path = None
_data_storage_path = None

InputDataType = str or List[str] or Dict[Any]


def __storage_path_by_os(purpose: StoragePurpose):
    return {
        "linux": os.path.expanduser(f"~/.{purpose.value}/hexagon"),
        "darwin": os.path.expanduser(f"~/.{purpose.value}/hexagon"),
        "cygwin": os.path.expanduser(f"~/.{purpose.value}/hexagon"),
        "win32": os.path.expanduser("~/hexagon"),
    }


def _get_storage_dir_path():
    global _config_storage_path
    if _config_storage_path:
        return _config_storage_path

    _config_storage_path = os.getenv(
        "HEXAGON_STORAGE_PATH",
        __storage_path_by_os(StoragePurpose.config)[sys.platform],
    )
    Path(_config_storage_path).mkdir(exist_ok=True)

    return _config_storage_path


def _resolve_storage_path(app: str, key: str, base_dir=None):
    base_dir = base_dir if base_dir else _get_storage_dir_path()
    key_split = key.split(".")
    return (os.path.join(base_dir, app, *key_split[:-1]), *key_split[-1:])


def _storage_value_type_by_data_type(data: InputDataType):
    if isinstance(data, str):
        return StorageValueType.text
    elif isinstance(data, list) and all(isinstance(s, str) for s in data):
        return StorageValueType.text_multiline
    elif isinstance(data, dict):
        return StorageValueType.dictionary
    else:
        raise Exception(
            f"Type {type(data).__name__} cannot be stored: supported types are str, List[str] or Dict"
        )


def _storage_value_type_by_file_path(file_path: str):
    if os.path.exists(file_path + ".txt"):
        return StorageValueType.text
    elif os.path.exists(file_path + ".yaml"):
        return StorageValueType.dictionary
    else:
        return None


def _storage_file(dir_path: str, file_name: str):
    base_file_path = os.path.join(dir_path, file_name)
    value_type = _storage_value_type_by_file_path(base_file_path)
    if not value_type:
        return None, None
    file_path = base_file_path + _extension_by_value_type[value_type]
    return file_path, value_type


def _get_app(app: str = None):
    from hexagon.domain import cli, configuration

    return (
        app
        if app
        else (
            cli.name.lower()
            if cli and configuration.has_config
            else HEXAGON_STORAGE_APP
        )
    )


def store_user_data(key: str, data: InputDataType, append=False, app: str = None):
    app = _get_app(app)

    value_type = _storage_value_type_by_data_type(data)
    extension = _extension_by_value_type[value_type]
    dir_path, file_name = _resolve_storage_path(app, key)
    file_name += extension
    file_path = os.path.join(dir_path, file_name)

    Path(dir_path).mkdir(exist_ok=True, parents=True)

    if (
        value_type == StorageValueType.text_multiline
        or value_type == StorageValueType.text
    ):
        with open(file_path, "a" if append else "w") as file:
            if isinstance(data, list):
                file.writelines(line + "\n" for line in data)
            else:
                file.write(data)

    elif value_type == StorageValueType.dictionary:
        previous = None
        if append and os.path.exists(file_path):
            with open(file_path, "r") as file:
                previous = YAML().load(file)

        to_write = merge_dictionaries_deep(previous, data) if previous else data

        with open(file_path, "w") as file:
            YAML().dump(to_write, file)


def load_user_data(key: str, app: str = None):
    app = _get_app(app)
    file_path, value_type = _storage_file(*_resolve_storage_path(app, key))

    if not value_type:
        return None

    if not os.path.isfile(file_path):
        return None

    with open(file_path, "r") as file:
        if (
            value_type == StorageValueType.text
            or value_type == StorageValueType.text_multiline
        ):
            lines = file.readlines()
            return (
                None
                if not lines or len(lines) == 0
                else (lines[0] if len(lines) == 1 else lines)
            )
        elif value_type == StorageValueType.dictionary:
            return YAML().load(file)


def delete_user_data(app: str, key: str):
    dir_path, file_name = _resolve_storage_path(app, key)
    full_path = os.path.join(dir_path, file_name)
    if os.path.isdir(full_path):
        rmtree(full_path)
    else:
        file_path, value_type = _storage_file(dir_path, file_name)
        if not value_type:
            return
        os.remove(file_path)


def clear_storage():
    storage_dir_path = _get_storage_dir_path()
    rmtree(storage_dir_path)
    os.mkdir(storage_dir_path)


def store_local_data(key: str, data: str):
    dir_path = get_local_data_dir()
    with open(os.path.join(dir_path, key), "a") as f:
        f.write(f"{data}\n")


def get_local_data_dir():
    dir_path = __storage_path_by_os(StoragePurpose.data)[sys.platform]
    Path(dir_path).mkdir(exist_ok=True, parents=True)
    return dir_path

import importlib
import os
import sys
from typing import List


def collect_plugins(project_path: str, plugins_list: List[str]):
    _import_all_in_folder(os.path.dirname(__file__))

    for plugin in plugins_list:
        plugins_dir_path = os.path.abspath(os.path.join(project_path, plugin))

        if os.path.isdir(plugins_dir_path):
            _import_all_in_folder(plugins_dir_path)
        elif os.path.isfile(plugins_dir_path):
            _import_plugin(plugin)


def _import_all_in_folder(path: str):
    sys.path.append(os.path.abspath(path))
    for module in os.listdir(path):
        _import_plugin(module)


def _import_plugin(module):
    name = os.path.splitext(module)[0]
    name = name.replace(os.path.sep, ".")

    if name != "__init__" and name != "__pycache__":
        imported = importlib.import_module(name)
        imported.main()

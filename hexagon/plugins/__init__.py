import importlib
import os
import sys

from hexagon.domain import cli, configuration


def _import_all_in_folder(path: str):
    sys.path.append(os.path.abspath(path))
    for module in os.listdir(path):
        name = module.split(".")[0]
        if name != "__init__" and name != "__pycache__":
            imported = importlib.import_module(name)
            imported.main()


def collect_plugins():
    _import_all_in_folder(os.path.dirname(__file__))

    if cli.plugins_dir:
        plugins_dir_path = os.path.abspath(
            os.path.join(configuration.project_path, cli.plugins_dir)
        )

        if os.path.exists(plugins_dir_path):
            _import_all_in_folder(plugins_dir_path)

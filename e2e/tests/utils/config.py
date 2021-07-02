import os
from e2e.tests.utils.path import e2e_test_folder_path
from ruamel.yaml import YAML


def write_hexagon_config(test_file: str, config):
    path = os.path.join(e2e_test_folder_path(test_file), "app.yml")
    with open(path, "w") as file:
        YAML().dump(config, file)

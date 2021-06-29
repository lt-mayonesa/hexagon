import os
from ruamel.yaml import YAML
from e2e.tests.utils.path import e2e_test_folder_path


def read_config_file(test_file: str):
    with open(os.path.join(e2e_test_folder_path(test_file), "app.yml"), "r") as file:
        return YAML().load(file)

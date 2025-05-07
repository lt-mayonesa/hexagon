import os

from ruamel.yaml import YAML

from tests_e2e.__specs.utils.path import e2e_test_folder_path


def write_hexagon_config(test_file: str, config):
    path = os.path.join(test_file, "app.yml")
    print("writing to", path)
    with open(path, "w") as file:
        YAML().dump(config, file)


def read_hexagon_config(test_file: str):
    with open(os.path.join(e2e_test_folder_path(test_file), "app.yml"), "r") as file:
        return YAML().load(file)

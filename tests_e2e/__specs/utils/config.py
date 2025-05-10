import os

from ruamel.yaml import YAML


def write_hexagon_config(test_file: str, config):
    path = os.path.join(test_file, "app.yml")
    print("writing to", path)
    with open(path, "w") as file:
        YAML().dump(config, file)


def read_hexagon_config(test_file: str):
    with open(os.path.join(test_file, "app.yml"), "r") as file:
        return YAML().load(file)

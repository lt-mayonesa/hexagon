import os
import sys

from ruamel.yaml import YAML


class Configuration:
    def __init__(self, path: str = None):
        self.project_path = path
        self.project_yaml = None
        self.custom_tools_path = None
        self.__config = None
        self.has_config = False

    def init_config(self, path: str):
        self.project_yaml = path
        self.project_path = os.path.dirname(self.project_yaml)

        __defaults = {
            "cli": {"name": "Hexagon"},
            "tools": {
                "save-alias": {
                    "long_name": "Save Last Command as Linux Alias",
                    "type": "hexagon",
                    "action": "hexagon.tools.internal.save_new_alias",
                },
                "create-tool": {
                    "long_name": "Create A New Tool",
                    "type": "hexagon",
                    "action": "hexagon.tools.internal.create_new_tool",
                },
            },
            "envs": {},
        }
        try:
            with open(path, "r") as f:
                self.__config = YAML().load(f)
                self.has_config = True
                if "custom_tools_dir" in self.__config["cli"]:
                    self.__register_custom_tools_path()
        except FileNotFoundError:
            return self.__initial_setup_config()

        return (
            {**__defaults["cli"], **self.__config["cli"]},
            {**self.__config["tools"], **__defaults["tools"]},
            {**__defaults["envs"], **self.__config["envs"]},
        )

    def refresh(self):
        return self.init_config(self.project_yaml)

    def save(self):
        with open(self.project_yaml, "w") as f:
            YAML().dump(self.__config, f)
        return self.__config["cli"], self.__config["tools"], self.__config["envs"]

    def add_tool(self, command, config):
        self.__config["tools"].insert(len(self.__config["tools"]), command, config)
        self.__config["tools"].yaml_set_comment_before_after_key(command, before="\n")

    def update_custom_tools_path(self, value, comment=None, position=0):
        self.__config["cli"].insert(position, "custom_tools_dir", value, comment)
        self.__register_custom_tools_path()

    def __register_custom_tools_path(self):
        self.custom_tools_path = os.path.abspath(
            os.path.join(self.project_path, self.__config["cli"]["custom_tools_dir"])
        )
        sys.path.append(self.custom_tools_path)

    @staticmethod
    def __initial_setup_config():
        return (
            {"name": "Hexagon"},
            {
                "install": {
                    "long_name": "Install CLI",
                    "description": "Install a custom project CLI from a YAML file.",
                    "type": "hexagon",
                    "action": "hexagon.tools.internal.install_cli",
                }
            },
            {},
        )

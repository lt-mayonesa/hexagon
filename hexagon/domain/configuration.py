import os
import sys
from typing import Any, List, Optional, Tuple, Union

from pydantic import BaseModel, ValidationError
from ruamel.yaml import YAML

from hexagon.domain.cli import Cli
from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool, GroupTool, Tool, ToolType
from hexagon.support.yaml import display_yaml_errors


class ConfigFile(BaseModel):
    cli: Cli
    envs: List[Env]
    tools: List[Union[ActionTool, GroupTool]]


class Configuration:
    __defaults = [
        ActionTool(
            name="save-alias",
            long_name="Save Last Command as Linux Alias",
            type=ToolType.hexagon,
            action="hexagon.actions.internal.save_new_alias",
        ),
        ActionTool(
            name="create-tool",
            long_name="Create A New Tool",
            type=ToolType.hexagon,
            action="hexagon.actions.internal.create_new_tool",
        ),
    ]

    def __init__(self, path: str = None):
        self.project_path = path
        self.project_yaml = None
        self.custom_tools_path = None
        self.__yaml = None
        self.__config: Optional[ConfigFile] = None

    def init_config(self, path: str) -> Tuple[Cli, List[Tool], List[Env]]:
        self.project_yaml = path
        self.project_path = os.path.dirname(self.project_yaml)

        try:
            self.__yaml = read_configuration_file(path)
            self.__config = ConfigFile(**self.__yaml)

            if self.__config.cli.custom_tools_dir:
                self.__register_custom_tools_path()
        except FileNotFoundError:
            return self.__initial_setup_config()
        except ValidationError as errors:
            display_yaml_errors(errors, self.__yaml, self.project_yaml)
            sys.exit(1)

        return (
            self.__config.cli,
            self.__config.tools + self.__defaults,
            self.__config.envs,
        )

    def refresh(self) -> Tuple[Cli, List[Tool], List[Env]]:
        return self.init_config(self.project_yaml)

    def save(self) -> Tuple[Cli, List[Tool], List[Env]]:
        with open(self.project_yaml, "w") as f:
            YAML().dump(self.__yaml, f)
        return (
            self.__config.cli,
            self.__config.tools + self.__defaults,
            self.__config.envs,
        )

    def add_tool(self, tool: Tool):
        self.__config.tools.append(tool)
        self.__yaml["tools"].append(tool.dict(exclude_none=True, exclude_unset=True))

    def update_custom_tools_path(self, value, comment=None, position=0):
        self.__config.cli.custom_tools_dir = value
        self.__yaml["cli"].insert(position, "custom_tools_dir", value, comment)
        self.__register_custom_tools_path()

    def __register_custom_tools_path(self):
        self.custom_tools_path = register_custom_tools_path(
            self.__config.cli.custom_tools_dir, self.project_path
        )

    @property
    def has_config(self):
        return self.__config is not None

    @staticmethod
    def __initial_setup_config() -> Tuple[Cli, List[Tool], List[Env]]:
        return (
            Cli(name="Hexagon", command="hexagon"),
            [
                ActionTool(
                    name="install",
                    long_name="Install CLI",
                    description="Install a custom project CLI from a YAML file.",
                    type=ToolType.hexagon,
                    action="hexagon.actions.internal.install_cli",
                )
            ],
            [],
        )


def read_configuration_file(path: str) -> Any:
    return YAML().load(open(path, "r"))


def register_custom_tools_path(path: str, realtive_to: str) -> str:
    absolute_path = os.path.abspath(os.path.join(realtive_to, path))
    sys.path.append(absolute_path)
    return absolute_path

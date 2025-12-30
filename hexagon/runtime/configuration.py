import os
import sys
from typing import List, Optional, Tuple, Union

from pydantic import BaseModel

from hexagon.domain.cli import Cli
from hexagon.domain.env import Env
from hexagon.domain.hexagon_error import ListHexagonError
from hexagon.domain.tool import (
    ActionTool,
    GroupTool,
    Tool,
    ToolType,
    ToolGroupConfigFile,
)
from hexagon.runtime.yaml import write_file, read_file, load_model


class ConfigFile(BaseModel):
    cli: Cli
    envs: List[Env]
    tools: List[Union[ActionTool, GroupTool]]


class GroupFileNotFoundError(ListHexagonError):
    def __init__(self, group_yaml_path: str):
        super().__init__(
            [
                _("error.domain.configuration.group_tool_file_not_found").format(
                    config_file_path=group_yaml_path
                )
            ]
        )


class Configuration:
    def __init__(self, path: str = None):
        self.project_path = path
        self.project_yaml = None
        self.custom_tools_path = None
        self.__yaml = None
        self.__config: Optional[ConfigFile] = None
        self.cwd_tools: List[Tool] = []

    def init_config(self, path: str) -> Tuple[Cli, List[Tool], List[Env]]:
        self.project_yaml = path
        self.project_path = os.path.dirname(self.project_yaml)

        self.__yaml = read_file(path)
        if not self.__yaml:
            return self.__initial_setup_config()

        self.__config = load_model(ConfigFile, self.__yaml, self.project_yaml)

        if self.__config.cli.custom_tools_dir:
            self.__register_custom_tools_path()

        self.__recursive_group_load(self.__config.tools)

        return self._configuration_tuple()

    def add_tools(self, tools: List[Tool]) -> Tuple[Cli, List[Tool], List[Env]]:
        self.cwd_tools += tools

        return self._configuration_tuple()

    def refresh(self) -> Tuple[Cli, List[Tool], List[Env]]:
        return self.init_config(self.project_yaml)

    def save(self) -> Tuple[Cli, List[Tool], List[Env]]:
        write_file(self.project_yaml, self.__yaml)
        return self._configuration_tuple()

    def add_tool(self, tool: Union[ActionTool, GroupTool]):
        self.__config.tools.append(tool)
        self.__yaml["tools"].append(
            tool.model_dump(mode="json", exclude_none=True, exclude_unset=True)
        )

    def update_custom_tools_path(self, value, comment=None, position=0):
        self.__config.cli.custom_tools_dir = value
        self.__yaml["cli"].insert(position, "custom_tools_dir", value, comment)
        self.__register_custom_tools_path()

    def _configuration_tuple(self):
        return (
            self.__config.cli,
            self.cwd_tools + self.__config.tools + self.__defaults,
            self.__config.envs,
        )

    @property
    def has_config(self):
        return self.__config is not None

    def __recursive_group_load(self, tools):
        for tool in tools:
            if tool.type == ToolType.group:
                if isinstance(tool.tools, str):
                    group_yaml_path = os.path.join(self.project_path, tool.tools)
                    group_config_yaml = read_file(group_yaml_path)

                    if not group_config_yaml:
                        raise GroupFileNotFoundError(group_yaml_path)

                    group_config = load_model(
                        ToolGroupConfigFile, group_config_yaml, group_yaml_path
                    )

                    tool.tools = group_config.tools
                self.__recursive_group_load(tool.tools)

    def __register_custom_tools_path(self):
        self.custom_tools_path = register_custom_tools_path(
            self.__config.cli.custom_tools_dir, self.project_path
        )

    @staticmethod
    def __initial_setup_config() -> Tuple[Cli, List[Tool], List[Env]]:
        def _tools():
            return [
                ActionTool(
                    name="install",
                    long_name=_("msg.domain.configuration.install_cli_long_name"),
                    description=_("msg.domain.configuration.install_cli_description"),
                    type=ToolType.hexagon,
                    action="hexagon.actions.internal.install_cli",
                ),
                ActionTool(
                    name="get-json-schema",
                    long_name=_("msg.domain.configuration.get_json_schema_long_name"),
                    description=_(
                        "msg.domain.configuration.get_json_schema_description"
                    ),
                    type=ToolType.hexagon,
                    action="hexagon.actions.internal.schema",
                ),
                ActionTool(
                    name="update-hexagon",
                    long_name=_("msg.domain.configuration.update_hexagon_long_name"),
                    type=ToolType.hexagon,
                    action="hexagon.actions.internal.update_hexagon",
                ),
            ]

        return (
            Cli(name="Hexagon", command="hexagon"),
            _tools(),
            [],
        )

    @property
    def __defaults(self):
        return [
            ActionTool(
                name="save-alias",
                long_name=_("msg.domain.configuration.save_alias_long_name"),
                type=ToolType.hexagon,
                action="hexagon.actions.internal.save_new_alias",
            ),
            ActionTool(
                name="replay",
                alias="r",
                long_name=_("msg.domain.configuration.replay_long_name"),
                type=ToolType.hexagon,
                action="hexagon.actions.internal.replay",
            ),
            ActionTool(
                name="create-tool",
                long_name=_("msg.domain.configuration.create_tool_long_name"),
                type=ToolType.hexagon,
                action="hexagon.actions.internal.create_new_tool",
            ),
            ActionTool(
                name="update-cli",
                long_name=_("msg.domain.configuration.update_cli_long_name"),
                type=ToolType.hexagon,
                action="hexagon.actions.internal.update_cli",
            ),
        ]


def register_custom_tools_path(path: str, realtive_to: str) -> str:
    absolute_path = os.path.abspath(os.path.join(realtive_to, path))
    sys.path.append(absolute_path)
    return absolute_path

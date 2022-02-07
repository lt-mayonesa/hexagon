import os
import sys
from typing import List, Tuple

from prompt_toolkit.validation import ValidationError

from hexagon.domain import envs, configuration
from hexagon.domain.configuration import (
    read_configuration_file,
    register_custom_tools_path,
)
from hexagon.domain.tool import (
    FunctionTool,
    GroupTool,
    Tool,
    ToolGroupConfigFile,
    ToolType,
)
from hexagon.domain.tool.execution import ToolExecutionParamters
from hexagon.support.execute.action import execute_action
from hexagon.support.hooks import HexagonHooks
from hexagon.support.printer import log
from hexagon.support.tracer import tracer
from hexagon.support.wax import search_by_name_or_alias, select_env, select_tool
from hexagon.support.yaml import display_yaml_errors


def select_and_execute_tool(
    tools: List[Tool],
    tool_argument: str = None,
    env_argument: str = None,
    arguments: List[object] = None,
    custom_tools_path: str = None,
) -> List[str]:
    arguments = arguments if arguments else []
    tool = search_by_name_or_alias(tools, tool_argument)
    env = search_by_name_or_alias(envs, env_argument)

    tool = select_tool(tools, tool)
    if tool.traced:
        tracer.tracing(tool.name)

    env, params = select_env(envs, tool.envs, env)

    if isinstance(tool, GroupTool):
        previous = tools, tool_argument, env_argument, arguments, custom_tools_path
        return _execute_group_tool(
            tool,
            # If the tool matched the tool argument, disable navigating back
            previous
            if not next((t for t in tools if t.name == tool_argument), None)
            else None,
            env_argument,
            arguments,
            custom_tools_path,
        )

    if isinstance(tool, FunctionTool):
        return tool.function()

    if env:
        tracer.tracing(env.name)

    HexagonHooks.before_tool_executed.run(
        ToolExecutionParamters(
            tool=tool,
            parameters=params,
            env=env,
            arguments=arguments,
            custom_tools_path=custom_tools_path,
        )
    )

    return execute_action(tool, params, env, arguments, custom_tools_path)


GO_BACK_TOOL = Tool(
    name="goback",
    long_name=_("msg.support.execute.tool.go_back_long_name"),
    type=ToolType.function,
    description=_("msg.support.execute.tool.go_back_description"),
    icon=_("icon.global.go_back"),
    traced=False,
)


def _execute_group_tool(
    tool: GroupTool,
    previous: Tuple[List[Tool], str, str, List[object], str] = None,
    env_argument: str = None,
    arguments: List[object] = None,
    previous_custom_tools_path: str = None,
) -> List[str]:
    config_file_path = os.path.join(configuration.project_path, tool.tools)

    try:
        group_config_yaml = read_configuration_file(config_file_path)
    except FileNotFoundError:
        # "File {config_file_path} could not be found"
        log.error(
            _("error.support.execute.tool.group_tool_file_not_found").format(
                config_file_path=config_file_path
            )
        )
        sys.exit(1)

    try:
        group_config = ToolGroupConfigFile(**group_config_yaml)
    except ValidationError as errors:
        display_yaml_errors(errors, group_config_yaml, config_file_path)
        sys.exit(1)

    # Shift cli args one place to the right
    tool_argument = env_argument
    env_argument = arguments[0] if len(arguments) > 0 else None
    sub_tool_arguments = arguments[1:]

    custom_tools_absolute_path = register_custom_tools_path(
        group_config.custom_tools_dir if group_config.custom_tools_dir else ".",
        os.path.dirname(tool.tools),
    )

    tools = group_config.tools

    if previous:

        def go_back():
            tracer.remove_last()
            select_and_execute_tool(*previous)

        tools = tools + [
            FunctionTool(**GO_BACK_TOOL.dict(), function=go_back),
        ]

    return select_and_execute_tool(
        tools,
        tool_argument,
        env_argument,
        sub_tool_arguments,
        custom_tools_absolute_path
        if custom_tools_absolute_path
        else previous_custom_tools_path,
    )

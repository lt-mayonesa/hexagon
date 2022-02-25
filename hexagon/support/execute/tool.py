from typing import List, Tuple

from hexagon.domain import envs
from hexagon.domain.tool import (
    FunctionTool,
    GroupTool,
    Tool,
    ToolType,
)
from hexagon.domain.tool.execution import ToolExecutionParameters
from hexagon.support.execute.action import execute_action
from hexagon.support.hooks import HexagonHooks
from hexagon.support.tracer import tracer
from hexagon.support.wax import search_by_name_or_alias, select_env, select_tool


def select_and_execute_tool(
    tools: List[Tool],
    tool_argument: str = None,
    env_argument: str = None,
    arguments: List[object] = None,
) -> List[str]:
    arguments = arguments if arguments else []
    tool = search_by_name_or_alias(tools, tool_argument)
    env = search_by_name_or_alias(envs, env_argument)

    tool = select_tool(tools, tool)
    if tool.traced:
        tracer.tracing(tool.name)

    env, params = select_env(envs, tool.envs, env)

    if isinstance(tool, GroupTool):
        previous = tools, tool_argument, env_argument, arguments
        return _execute_group_tool(
            tool,
            # If the tool matched the tool argument, disable navigating back
            previous
            if not next((t for t in tools if t.name == tool_argument), None)
            else None,
            env_argument,
            arguments,
        )

    if isinstance(tool, FunctionTool):
        return tool.function()

    if env:
        tracer.tracing(env.name)

    HexagonHooks.before_tool_executed.run(
        ToolExecutionParameters(
            tool=tool, parameters=params, env=env, arguments=arguments,
        )
    )

    return execute_action(tool, params, env, arguments)


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
) -> List[str]:

    # Shift cli args one place to the right
    tool_argument = env_argument
    env_argument = arguments[0] if len(arguments) > 0 else None
    sub_tool_arguments = arguments[1:]

    tools = tool.tools

    if previous:

        def go_back():
            tracer.remove_last()
            select_and_execute_tool(*previous)

        # FunctionTool is not set as a type GroupTool.tools
        # so yaml validations dont show that tool.function is required
        # noinspection PyTypeChecker
        tools = tool.tools + [
            FunctionTool(**GO_BACK_TOOL.dict(), function=go_back),
        ]

    return select_and_execute_tool(
        tools, tool_argument, env_argument, sub_tool_arguments,
    )

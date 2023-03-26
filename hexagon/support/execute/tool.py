from typing import List, Tuple

from hexagon.domain import envs
from hexagon.domain.tool import (
    FunctionTool,
    GroupTool,
    Tool,
    ToolType,
)
from hexagon.domain.tool.execution import ToolExecutionParameters
from hexagon.support.args import CliArgs, parse_cli_args
from hexagon.support.execute.action import execute_action
from hexagon.support.hooks import HexagonHooks
from hexagon.support.tracer import tracer
from hexagon.support.wax import search_by_name_or_alias, select_env, select_tool


def select_and_execute_tool(
    tools: List[Tool],
    cli_args: CliArgs,
) -> List[str]:
    tool = search_by_name_or_alias(tools, cli_args.tool)
    env = search_by_name_or_alias(envs, cli_args.env)

    tool = select_tool(tools, tool)
    if tool.traced:
        tracer.tracing(tool.name)

    env, tool_env_params = select_env(envs, tool.envs, env)

    if isinstance(tool, GroupTool):
        previous = tools, cli_args
        return _execute_group_tool(
            tool,
            cli_args,
            # If the tool matched the tool argument, disable navigating back
            previous=previous
            if not next((t for t in tools if t.name == cli_args.tool), None)
            else None,
        )

    if isinstance(tool, FunctionTool):
        return tool.function()

    if env:
        tracer.tracing(env.name)

    HexagonHooks.before_tool_executed.run(
        ToolExecutionParameters(
            tool=tool,
            parameters=tool_env_params,
            env=env,
            arguments=cli_args.extra_args,
        )
    )

    return execute_action(tool, tool_env_params, env, cli_args)


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
    cli_args: CliArgs,
    previous: Tuple[List[Tool], str, str, List[object], str] = None,
) -> List[str]:
    tools = tool.tools

    if previous:

        def go_back():
            tracer.remove_last()
            select_and_execute_tool(*previous)

        # FunctionTool is not set as a type GroupTool.tools
        # so yaml validations don't show that tool.function is required
        # noinspection PyTypeChecker
        tools = tool.tools + [
            FunctionTool(**GO_BACK_TOOL.dict(), function=go_back),
        ]

    return select_and_execute_tool(
        tools,
        parse_cli_args([cli_args.env] + cli_args.raw_extra_args),
    )

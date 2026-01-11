from typing import List, Tuple

from hexagon.domain.env import Env
from hexagon.domain.hooks.execution import ToolExecutionParameters
from hexagon.domain.tool import (
    FunctionTool,
    GroupTool,
    Tool,
    ToolType,
)
from hexagon.runtime.execute.action import execute_action
from hexagon.runtime.parse_args import parse_cli_args
from hexagon.runtime.presentation.tool_display import prepare_tools_for_display
from hexagon.runtime.wax import search_by_name_or_alias, select_env, select_tool
from hexagon.support.hooks import HexagonHooks
from hexagon.support.input.args import CliArgs
from hexagon.support.tracer import tracer


def _build_tools_to_trace(tool: Tool, group_ref: int):
    """
    Build a collection of tools to trace (group path + final tool).

    Returns a list of tuples (key, name, alias) for each tool in the path.
    """

    def _trace_tuple(gr: int, t) -> tuple[str, str, str | None]:
        return f"tool_{gr}", t.name, t.alias

    if not tool.group_path:
        return [_trace_tuple(group_ref, tool)]

    group_trace = [
        _trace_tuple(group_ref + i, group_item)
        for i, group_item in enumerate(tool.group_path)
    ]
    selected_tool = [_trace_tuple(group_ref + len(tool.group_path), tool)]

    return group_trace + selected_tool


def select_and_execute_tool(
    tools: List[Tool],
    envs: List[Env],
    cli_args: CliArgs,
    group_ref=0,
) -> List[str]:
    display_tools = prepare_tools_for_display(tools)

    tool = search_by_name_or_alias(display_tools, cli_args.tool and cli_args.tool.value)
    env = search_by_name_or_alias(envs, cli_args.env and cli_args.env.value)

    tool = select_tool(display_tools, tool)
    if tool.traced:
        for key, name, alias in _build_tools_to_trace(tool, group_ref):
            tracer().tracing(key, name, value_alias=alias)

    env, tool_env_params = select_env(envs, tool.envs, env)

    if isinstance(tool, GroupTool):
        previous = tools, envs, cli_args
        return _execute_group_tool(
            tool,
            envs,
            cli_args,
            ref=group_ref + 1,
            # If the tool matched the tool argument, disable navigating back
            previous=(
                previous
                if not next(
                    (
                        t
                        for t in tools
                        if cli_args.tool and t.name == cli_args.tool.value
                    ),
                    None,
                )
                else None
            ),
        )

    if isinstance(tool, FunctionTool):
        return tool.function()

    if env:
        tracer().tracing(f"env_{group_ref}", env.name, value_alias=env.alias)

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
    envs: List[Env],
    cli_args: CliArgs,
    ref,
    previous: Tuple = None,
) -> List[str]:
    tools = tool.tools

    if previous:

        def go_back():
            tracer().remove_last()
            select_and_execute_tool(*previous)

        # FunctionTool is not set as a type GroupTool.tools
        # so yaml validations don't show that tool.function is required
        # noinspection PyTypeChecker
        tools = tool.tools + [
            FunctionTool(**GO_BACK_TOOL.model_dump(), function=go_back),
        ]

    return select_and_execute_tool(
        tools,
        envs,
        parse_cli_args(
            ([cli_args.env.value] if cli_args.env else []) + cli_args.raw_extra_args
        ),
        group_ref=ref,
    )

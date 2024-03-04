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
from hexagon.support.input.args import CliArgs
from hexagon.runtime.wax import search_by_name_or_alias, select_env, select_tool
from hexagon.support.hooks import HexagonHooks
from hexagon.support.tracer import tracer


def select_and_execute_tool(
    tools: List[Tool],
    envs: List[Env],
    cli_args: CliArgs,
    group_ref=0,
) -> List[str]:
    tool = search_by_name_or_alias(tools, cli_args.tool and cli_args.tool.value)
    env = search_by_name_or_alias(envs, cli_args.env and cli_args.env.value)
    # FIXME: validate selected env: if tool has envs defined and env is None -> should fail

    tool = select_tool(tools, tool)
    if tool.traced:
        tracer().tracing(f"tool_{group_ref}", tool.name, value_alias=tool.alias)

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
            FunctionTool(**GO_BACK_TOOL.dict(), function=go_back),
        ]

    return select_and_execute_tool(
        tools,
        envs,
        parse_cli_args(
            ([cli_args.env.value] if cli_args.env else []) + cli_args.raw_extra_args
        ),
        group_ref=ref,
    )

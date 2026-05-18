from typing import List, Optional, Tuple, Union

from hexagon.domain.env import Env
from hexagon.domain.hooks.execution import ToolExecutionParameters
from hexagon.domain.tool import FunctionTool, GroupTool, Separator, Tool, ToolType
from hexagon.runtime.execute.action import execute_action
from hexagon.runtime.parse_args import parse_cli_args
from hexagon.runtime.wax import _select_and_register_event, search_by_name_or_alias
from hexagon.support.hooks import HexagonHooks
from hexagon.support.input.args import CliArgs
from hexagon.support.tracer import tracer


def _tool_classifier(tool: Union[Tool, Env]) -> str:
    if tool.icon:
        return f"{tool.icon:2}"
    symbols = {"web": "⦾", "shell": "ƒ", "misc": " ", "hexagon": "⬡", "group": "≡"}
    r = symbols.get(tool.type, "")
    return f"{r:2}" if r else ""


def _display_choices(
    items: List[Union[Tool, Env]], classifier=lambda _: ""
) -> List[dict]:
    def build_name(v: Union[Tool, Env]) -> str:
        gap = 60 if v.description else 0
        return f"{classifier(v) + (v.long_name or v.name): <{gap}}{v.description or ''}"

    return [
        {"value": item.name, "name": build_name(item)}
        for item in items
        if Separator.name not in item.name
    ]


def _ensure_prompt(cli_args: CliArgs) -> None:
    """Lazily initialize a Prompt on cli_args when one has not been set.

    ``__main__.py`` always calls ``_with_prompt()`` before
    ``select_and_execute_tool``, so this guard is a no-op in the normal flow.
    It exists for callers like ``replay.py`` that invoke
    ``select_and_execute_tool`` directly with a raw ``parse_cli_args()`` result.
    If the replayed tool no longer exists the selection falls through to an
    interactive prompt, which requires a ``Prompt`` instance.
    """
    if not cli_args.__prompt__:
        from hexagon.support.input.prompt import Prompt

        cli_args._with_prompt(Prompt())


def select_and_execute_tool(
    tools: List[Tool],
    envs: List[Env],
    cli_args: CliArgs,
    group_ref=0,
) -> List[str]:
    _ensure_prompt(cli_args)
    found_tool_name = search_by_name_or_alias(
        tools, cli_args.tool and cli_args.tool.value
    )
    tool_was_prompted = not found_tool_name

    if not found_tool_name:
        found_tool_name = cli_args.tool.prompt(
            choices=_display_choices(tools, classifier=_tool_classifier),
            searchable=True,
            message=_("action.support.wax.select_tool"),
        )

    tool = _select_and_register_event(
        found_tool_name, tools, target="tool", prompted=tool_was_prompted
    )

    if tool.traced:
        tracer().tracing(f"tool_{group_ref}", tool.name, value_alias=tool.alias)

    if isinstance(tool, GroupTool):
        if tool_was_prompted:
            # Reset so that go_back() re-prompts the parent menu rather than
            # navigating directly back into this group.
            cli_args.tool = None
        previous = tools, envs, cli_args
        return _execute_group_tool(
            tool,
            envs,
            cli_args,
            ref=group_ref + 1,
            previous=previous if tool_was_prompted else None,
        )

    if isinstance(tool, FunctionTool):
        return tool.function()

    env, tool_env_params = _resolve_env(envs, tool.envs, cli_args)

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


def _resolve_env(
    available_envs: List[Env],
    tool_envs: Optional[dict],
    cli_args: CliArgs,
) -> Tuple[Optional[Env], Optional[str]]:
    if not tool_envs:
        return None, None

    if "*" in tool_envs:
        return None, tool_envs["*"]

    found_env_name = search_by_name_or_alias(
        available_envs, cli_args.env and cli_args.env.value
    )
    env_was_prompted = not found_env_name

    if not found_env_name:
        eligible = [e for e in available_envs if e.name in tool_envs]
        found_env_name = cli_args.env.prompt(
            choices=_display_choices(eligible),
            searchable=True,
            message=_("action.support.wax.select_environment"),
        )

    env = _select_and_register_event(
        found_env_name, available_envs, target="env", prompted=env_was_prompted
    )
    return env, tool_envs[found_env_name]


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
    ref: int,
    previous: Optional[Tuple] = None,
) -> List[str]:
    tools = tool.tools

    if previous:

        def go_back():
            tracer().remove_last()
            select_and_execute_tool(*previous)

        # noinspection PyTypeChecker
        tools = tool.tools + [
            FunctionTool(**GO_BACK_TOOL.dict(), function=go_back),
        ]

    inner_args = parse_cli_args(
        ([cli_args.env.value] if cli_args.env.value else []) + cli_args.raw_extra_args
    )._with_prompt(cli_args.__prompt__)

    return select_and_execute_tool(tools, envs, inner_args, group_ref=ref)

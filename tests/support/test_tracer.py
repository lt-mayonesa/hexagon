import pytest

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool, GroupTool, ToolType
from hexagon.support.parse_args import parse_cli_args
from hexagon.support.tracer import Tracer

tools_dict = [
    ActionTool(name="docker", alias="d", action="docker", type=ToolType.shell),
    ActionTool(name="bastion", alias="b", action="sarasa", type=ToolType.shell),
    ActionTool(name="no-alias", action="sarasa", type=ToolType.shell),
    GroupTool(
        name="tool-group",
        alias="tg",
        type=ToolType.group,
        tools=[
            ActionTool(name="one", alias="o", action="tool_one"),
            ActionTool(name="two", alias="t", action="tool_two"),
        ],
    ),
    GroupTool(
        name="tool-group-envs",
        alias="tge",
        type=ToolType.group,
        envs={"dev": "value dev", "qa": "value qa"},
        tools=[
            ActionTool(
                name="one",
                alias="o",
                action="tool_one",
            ),
            ActionTool(
                name="two",
                alias="t",
                action="tool_two",
                envs={"dev": "val dev", "qa": "val qa"},
            ),
            GroupTool(
                name="tool-group-inner",
                alias="tgi",
                type=ToolType.group,
                envs={"dev": "inner dev", "qa": "inner qa"},
                tools=[
                    ActionTool(
                        name="inner_one",
                        alias="io",
                        action="tool_one",
                    ),
                    ActionTool(
                        name="inner_two",
                        alias="it",
                        action="tool_two",
                        envs={"dev": "val dev", "qa": "val qa"},
                    ),
                ],
            ),
        ],
    ),
]

envs_dict = [Env(name="dev", alias="d"), Env(name="qa", alias="q")]


@pytest.mark.parametrize(
    "initial,expected_trace",
    [
        (parse_cli_args([]), ""),
        (parse_cli_args(["docker"]), ""),
        (parse_cli_args(["docker", "dev"]), ""),
    ],
)
def test_build_command_from_initial_trace(initial, expected_trace):
    tracer = Tracer(initial)
    assert tracer.trace() == expected_trace
    assert tracer.aliases_trace(tools_dict, envs_dict) == expected_trace


@pytest.mark.parametrize(
    "args,traces,has_traced,expected_trace,expected_alias",
    [
        (parse_cli_args([]), [], False, "", ""),
        (parse_cli_args(["docker"]), ["docker"], False, "docker", "d"),
        (parse_cli_args([]), ["no-alias"], True, "no-alias", "no-alias"),
        (
            parse_cli_args(["docker", "dev"]),
            ["docker", "dev", "something"],
            True,
            "docker dev something",
            "d d something",
        ),
        (
            parse_cli_args(["docker", "dev", "--foo", "bar"]),
            ["docker", "dev", ("foo", "bar")],
            True,
            "docker dev --foo=bar",
            "d d --foo=bar",
        ),
        (
            parse_cli_args(["docker", "dev", "--foo=bar", "--foo=baz"]),
            ["docker", "dev", ("foo", ["bar", "baz"])],
            False,
            "docker dev --foo=bar --foo=baz",
            "d d --foo=bar --foo=baz",
        ),
        (
            parse_cli_args(
                ["docker", "dev", "--foo", "bar", "--bar", "baz", "my-value"]
            ),
            ["docker", "dev", ("foo", "bar"), ("bar", "baz"), "my-value"],
            True,
            "docker dev --foo=bar --bar=baz my-value",
            "d d --foo=bar --bar=baz my-value",
        ),
        (
            parse_cli_args(["tool-group", "one"]),
            ["tool-group", "one"],
            False,
            "tool-group one",
            "tg o",
        ),
        (parse_cli_args([]), ["tool-group", "one"], True, "tool-group one", "tg o"),
        (
            parse_cli_args([]),
            ["tool-group-envs", "dev", "one"],
            True,
            "tool-group-envs dev one",
            "tge d o",
        ),
        (
            parse_cli_args([]),
            ["tool-group-envs", "qa", "two", "dev"],
            True,
            "tool-group-envs qa two dev",
            "tge q t d",
        ),
        (
            parse_cli_args([]),
            ["tool-group-envs", "qa", "tool-group-inner", "qa", "inner_two", "dev"],
            True,
            "tool-group-envs qa tool-group-inner qa inner_two dev",
            "tge q tgi q it d",
        ),
    ],
)
def test_build_command_from_traced(
    args, traces, has_traced, expected_trace, expected_alias
):
    tracer = Tracer(args)
    for t in traces:
        if isinstance(t, tuple):
            tracer.tracing(t[1], key=t[0])
        else:
            tracer.tracing(t)
    assert tracer.has_traced() == has_traced
    assert tracer.trace() == expected_trace
    assert tracer.aliases_trace(tools_dict, envs_dict) == expected_alias

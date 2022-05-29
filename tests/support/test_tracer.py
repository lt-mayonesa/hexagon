import pytest

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool, GroupTool, ToolType
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
    "initial,expected_command",
    [([], ""), ([""], ""), (["docker"], ""), (["docker", "dev"], "")],
)
def test_build_command_from_initial_trace(initial, expected_command):
    tracer = Tracer(initial)
    assert tracer.command() == expected_command
    assert tracer.command_as_aliases(tools_dict, envs_dict) == expected_command


@pytest.mark.parametrize(
    "initial,traced,has_traced,expected_command,expected_alias",
    [
        ([], [], False, "", ""),
        ([""], [""], False, "", ""),
        (["docker"], ["docker"], False, "docker", "d"),
        ([], ["no-alias"], True, "no-alias", "no-alias"),
        (
            ["docker", "dev"],
            ["docker", "dev", "something"],
            True,
            "docker dev something",
            "d d something",
        ),
        (["tool-group", "one"], ["tool-group", "one"], False, "tool-group one", "tg o"),
        ([], ["tool-group", "one"], True, "tool-group one", "tg o"),
        (
            [],
            ["tool-group-envs", "dev", "one"],
            True,
            "tool-group-envs dev one",
            "tge d o",
        ),
        (
            [],
            ["tool-group-envs", "qa", "two", "dev"],
            True,
            "tool-group-envs qa two dev",
            "tge q t d",
        ),
        (
            [],
            ["tool-group-envs", "qa", "tool-group-inner", "qa", "inner_two", "dev"],
            True,
            "tool-group-envs qa tool-group-inner qa inner_two dev",
            "tge q tgi q it d",
        ),
    ],
)
def test_build_command_from_traced(
    initial, traced, has_traced, expected_command, expected_alias
):
    tracer = Tracer(initial)
    for t in traced:
        tracer.tracing(t)
    assert tracer.has_traced() == has_traced
    assert tracer.command() == expected_command
    assert tracer.command_as_aliases(tools_dict, envs_dict) == expected_alias

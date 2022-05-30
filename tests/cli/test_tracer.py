import pytest

from hexagon.domain.tool import Tool
from hexagon.domain.env import Env
from hexagon.support.tracer import Tracer

tools_dict = [
    Tool(name="docker", alias="d", action="docker"),
    Tool(name="bastion", alias="b", action="sarasa"),
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
        (
            ["docker", "dev"],
            ["docker", "dev", "something"],
            True,
            "docker dev something",
            "d d something",
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

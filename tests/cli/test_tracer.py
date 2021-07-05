import pytest

from hexagon.support.tracer import Tracer

tools_dict = {"docker": {"alias": "d"}, "bastion": {"alias": "b"}}

envs_dict = {"dev": {"alias": "d"}, "qa": {"alias": "q"}}


@pytest.mark.parametrize(
    "initial,expected_command",
    [
        ([], ""),
        ([""], ""),
        (["docker"], ""),
        (["docker", "dev"], ""),
    ],
)
def test_build_command_from_initial_trace(initial, expected_command):
    tracer = Tracer(initial)
    assert tracer.command() == expected_command
    assert tracer.command_as_aliases(tools_dict, envs_dict) == expected_command

import pytest

from hexagon.support.parse_args import parse_cli_args
from hexagon.support.tracer import Tracer


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
    assert tracer.aliases_trace() == expected_trace


@pytest.mark.parametrize(
    "args,traces,has_traced,expected_trace,expected_alias",
    [
        (parse_cli_args([]), [], False, "", ""),
        (
            parse_cli_args(["docker"]),
            [("tool", "docker", None, "d", None)],
            False,
            "docker",
            "d",
        ),
        (
            parse_cli_args([]),
            [("tool", "no-alias", None, None, None)],
            True,
            "no-alias",
            "no-alias",
        ),
        (
            parse_cli_args(["docker", "dev"]),
            [
                ("tool", "docker", None, "d", None),
                ("env", "dev", None, "d", None),
                ("arg1", "something", None, None, None),
            ],
            True,
            "docker dev something",
            "d d something",
        ),
        (
            parse_cli_args(["docker", "dev", "--foo", "bar"]),
            [
                ("tool", "docker", None, "d", None),
                ("env", "dev", None, "d", None),
                ("foo", "bar", "--foo", None, None),
            ],
            False,
            "docker dev --foo=bar",
            "d d --foo=bar",
        ),
        (
            parse_cli_args(["docker", "dev", "--foo=bar", "--foo=baz"]),
            [
                ("tool", "docker", None, "d", None),
                ("env", "dev", None, "d", None),
                ("foo", ["bar", "baz"], "--foo", None, None),
            ],
            False,
            "docker dev --foo=bar --foo=baz",
            "d d --foo=bar --foo=baz",
        ),
        (
            parse_cli_args(["docker", "dev", "--foo=bar", "--bar=baz", "my-value"]),
            [
                ("tool", "docker", None, "d", None),
                ("env", "dev", None, "d", None),
                ("foo", "bar", "--foo", None, "-f"),
                ("bar", "baz", "--bar", None, "-f"),
                ("arg1", "my-value", None, None, None),
            ],
            False,
            "docker dev --foo=bar --bar=baz my-value",
            "d d -f=bar -f=baz my-value",
        ),
        (
            parse_cli_args(
                ["docker", "dev", "--foo", "bar", "--bar", "baz", "my-value"]
            ),
            [
                ("tool", "docker", None, "d", None),
                ("env", "dev", None, "d", None),
                ("foo", "bar", "--foo", None, "-f"),
                ("bar", "baz", "--bar", None, "-f"),
                ("arg1", "my-value", None, None, None),
            ],
            False,
            "docker dev --foo=bar --bar=baz my-value",
            "d d -f=bar -f=baz my-value",
        ),
        (
            parse_cli_args(["tool-group", "one"]),
            [
                ("tool", "tool-group", None, "tg", None),
                ("env", "one", None, "o", None),
            ],
            False,
            "tool-group one",
            "tg o",
        ),
        (
            parse_cli_args([]),
            [
                ("tool", "tool-group", None, "tg", None),
                ("env", "one", None, "o", None),
            ],
            True,
            "tool-group one",
            "tg o",
        ),
        (
            parse_cli_args([]),
            [
                ("tool", "tool-group-envs", None, "tge", None),
                ("env", "dev", None, "d", None),
                ("group1", "one", None, "o", None),
            ],
            True,
            "tool-group-envs dev one",
            "tge d o",
        ),
        (
            parse_cli_args(["docker", "dev", "-f", "bar", "-b", "baz", "my-value"]),
            [
                ("tool", "docker", None, "d", None),
                ("env", "dev", None, "d", None),
                ("foo", "bar", "--foo", None, "-f"),
                ("bar", "baz", "--bar", None, "-f"),
                ("arg1", "my-value", None, None, None),
            ],
            False,
            "docker dev --foo=bar --bar=baz my-value",
            "d d -f=bar -f=baz my-value",
        ),
    ],
)
def test_build_command_from_traced(
    args, traces, has_traced, expected_trace, expected_alias
):
    tracer = Tracer(args)
    for t in traces:
        tracer.tracing(*t)
    assert tracer.trace() == expected_trace
    assert tracer.aliases_trace() == expected_alias
    assert tracer.has_traced() == has_traced


def test_trace_same_key_multiple_times():
    tracer = Tracer(parse_cli_args([]))
    tracer.tracing("name", "John", key="--name", key_alias="-n")
    tracer.tracing("name", "Charles", key="--name", key_alias="-n")
    tracer.tracing("name", "Richard", key="--name", key_alias="-n")
    tracer.tracing("name", "Bob", key="--name", key_alias="-n")
    assert tracer.trace() == "--name=Bob"
    assert tracer.aliases_trace() == "-n=Bob"
    assert tracer.has_traced() is True

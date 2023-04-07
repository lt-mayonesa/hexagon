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
            [("docker", None, "d", None)],
            False,
            "docker",
            "d",
        ),
        (
            parse_cli_args([]),
            [("no-alias", None, None, None)],
            True,
            "no-alias",
            "no-alias",
        ),
        (
            parse_cli_args(["docker", "dev"]),
            [
                ("docker", None, "d", None),
                ("dev", None, "d", None),
                ("something", None, None, None),
            ],
            True,
            "docker dev something",
            "d d something",
        ),
        (
            parse_cli_args(["docker", "dev", "--foo", "bar"]),
            [
                ("docker", None, "d", None),
                ("dev", None, "d", None),
                ("bar", "--foo", None, None),
            ],
            False,
            "docker dev --foo=bar",
            "d d --foo=bar",
        ),
        (
            parse_cli_args(["docker", "dev", "--foo=bar", "--foo=baz"]),
            [
                ("docker", None, "d", None),
                ("dev", None, "d", None),
                (["bar", "baz"], "--foo", None, None),
            ],
            False,
            "docker dev --foo=bar --foo=baz",
            "d d --foo=bar --foo=baz",
        ),
        (
            parse_cli_args(["docker", "dev", "--foo=bar", "--bar=baz", "my-value"]),
            [
                ("docker", None, "d", None),
                ("dev", None, "d", None),
                ("bar", "--foo", None, "-f"),
                ("baz", "--bar", None, "-f"),
                ("my-value", None, None, None),
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
                ("docker", None, "d", None),
                ("dev", None, "d", None),
                ("bar", "--foo", None, "-f"),
                ("baz", "--bar", None, "-f"),
                ("my-value", None, None, None),
            ],
            False,
            "docker dev --foo=bar --bar=baz my-value",
            "d d -f=bar -f=baz my-value",
        ),
        (
            parse_cli_args(["tool-group", "one"]),
            [
                ("tool-group", None, "tg", None),
                ("one", None, "o", None),
            ],
            False,
            "tool-group one",
            "tg o",
        ),
        (
            parse_cli_args([]),
            [
                ("tool-group", None, "tg", None),
                ("one", None, "o", None),
            ],
            True,
            "tool-group one",
            "tg o",
        ),
        (
            parse_cli_args([]),
            [
                ("tool-group-envs", None, "tge", None),
                ("dev", None, "d", None),
                ("one", None, "o", None),
            ],
            True,
            "tool-group-envs dev one",
            "tge d o",
        ),
        (
            parse_cli_args(["docker", "dev", "-f", "bar", "-b", "baz", "my-value"]),
            [
                ("docker", None, "d", None),
                ("dev", None, "d", None),
                ("bar", "--foo", None, "-f"),
                ("baz", "--bar", None, "-f"),
                ("my-value", None, None, None),
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

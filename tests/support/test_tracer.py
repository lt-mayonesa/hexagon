from enum import Enum

import pytest

from hexagon.runtime.parse_args import parse_cli_args
from hexagon.support.tracer import Tracer


@pytest.mark.parametrize(
    "initial,expected_trace",
    [
        (parse_cli_args([]), ""),
        (parse_cli_args(["docker"]), ""),
        (parse_cli_args(["docker", "dev"]), ""),
    ],
)
def test_tracer_returns_empty_string_for_initial_cli_args_without_tracing(
    initial, expected_trace
):
    """
    Given a Tracer initialized with CLI arguments (empty, 'docker', or 'docker dev').
    When trace() and aliases_trace() are called without any tracing being done.
    Then both methods should return an empty string.
    """
    tracer = Tracer(initial)
    assert tracer.trace() == expected_trace
    assert tracer.aliases_trace() == expected_trace


class MyEnum(Enum):
    A = "a"
    B = "b"
    C = "c"


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
def test_tracer_builds_command_string_from_traced_values(
    args, traces, has_traced, expected_trace, expected_alias
):
    """
    Given a Tracer initialized with specific CLI arguments.
    When multiple values are traced using the tracing() method.
    Then trace() should return a command string with full argument names.
    And aliases_trace() should return a command string with aliased argument names.
    And has_traced() should return whether any tracing was done without CLI args.
    """
    tracer = Tracer(args)
    for t in traces:
        tracer.tracing(*t)
    assert tracer.trace() == expected_trace
    assert tracer.aliases_trace() == expected_alias
    assert tracer.has_traced() == has_traced


def test_tracer_keeps_only_last_value_when_same_key_is_traced_multiple_times():
    """
    Given a Tracer initialized with empty CLI arguments.
    When the same key 'name' is traced multiple times with different values.
    Then trace() should return a command string with only the last value.
    And aliases_trace() should return a command string with the aliased key and only the last value.
    And has_traced() should return True.
    """
    tracer = Tracer(parse_cli_args([]))
    tracer.tracing("name", "John", key="--name", key_alias="-n")
    tracer.tracing("name", "Charles", key="--name", key_alias="-n")
    tracer.tracing("name", "Richard", key="--name", key_alias="-n")
    tracer.tracing("name", "Bob", key="--name", key_alias="-n")
    assert tracer.trace() == "--name=Bob"
    assert tracer.aliases_trace() == "-n=Bob"
    assert tracer.has_traced() is True


def test_tracer_converts_enum_value_to_its_string_representation():
    """
    Given a Tracer initialized with empty CLI arguments.
    When an enum value MyEnum.B is traced without a key.
    Then trace() should return the enum's string value 'b'.
    And aliases_trace() should also return the enum's string value 'b'.
    And has_traced() should return True.
    """
    tracer = Tracer(parse_cli_args([]))
    tracer.tracing(ref="name", value=MyEnum.B)
    assert tracer.trace() == "b"
    assert tracer.aliases_trace() == "b"
    assert tracer.has_traced() is True


def test_tracer_formats_enum_value_with_key_when_key_is_provided():
    """
    Given a Tracer initialized with empty CLI arguments.
    When an enum value MyEnum.A is traced with key='--name' and key_alias='-n'.
    Then trace() should return '--name=a' with the enum's string value.
    And aliases_trace() should return '-n=a' with the aliased key and enum's string value.
    And has_traced() should return True.
    """
    tracer = Tracer(parse_cli_args([]))
    tracer.tracing("name", MyEnum.A, key="--name", key_alias="-n")
    assert tracer.trace() == "--name=a"
    assert tracer.aliases_trace() == "-n=a"
    assert tracer.has_traced() is True


def test_tracer_converts_boolean_value_to_string_representation():
    """
    Given a Tracer initialized with empty CLI arguments.
    When a boolean value True is traced with ref='proceed'.
    Then trace() should return the string 'true'.
    And aliases_trace() should also return the string 'true'.
    And has_traced() should return True.
    """
    tracer = Tracer(parse_cli_args([]))
    tracer.tracing(ref="proceed", value=True)
    assert tracer.trace() == "true"
    assert tracer.aliases_trace() == "true"
    assert tracer.has_traced() is True

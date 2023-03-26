import pytest

from hexagon.support.args import parse_cli_args


def test_no_cli_args_passed():
    actual = parse_cli_args([])
    assert actual.tool is None
    assert actual.env is None
    assert actual.extra_args is None


@pytest.mark.parametrize(
    "args,expected",
    [
        (["some-tool"], "some-tool"),
        (["some-env"], "some-env"),
        (["123"], "123"),
    ],
)
def test_cli_args_only_tool_passed(args, expected):
    actual = parse_cli_args(args)
    assert actual.tool is expected
    assert actual.env is None
    assert actual.extra_args is None


@pytest.mark.parametrize(
    "args",
    [
        (["my tool with spaces"]),
        (["my!tool"]),
        (["my@tool"]),
        (["(@*#&$)!~(%&!%#)"]),
        (["(#)"]),
        (["valid_tool", "my env with spaces"]),
        (["valid_tool", "my!env"]),
        (["valid_tool", "my@env"]),
        (["valid_tool", "(@*#&$)!~(%&!%#)"]),
        (["valid_tool", "(#)"]),
    ],
)
def test_cli_args_handle_invalid_args(args):
    with pytest.raises(SystemExit, match="2"):
        parse_cli_args(args)


def test_cli_args_tool_is_first_argument_2():
    actual = parse_cli_args(["some-env", "some-tool"])
    assert actual.tool is "some-env"
    assert actual.env is "some-tool"
    assert actual.extra_args is None


def test_cli_args_env_is_second_positional_argument():
    actual = parse_cli_args(["some-tool", "some-env"])
    assert actual.tool is "some-tool"
    assert actual.env is "some-env"
    assert actual.extra_args is None


@pytest.mark.parametrize(
    "optional_args,expected",
    [
        ([], None),
        (["--number", "123"], {"number": "123"}),
        (["123", "--number", "123"], {"0": "123", "number": "123"}),
        (
            ["zero", "one", "two", "three"],
            {"0": "zero", "1": "one", "2": "two", "3": "three"},
        ),
        (
            ["zero", "zero", "zero", "zero"],
            {"0": "zero", "1": "zero", "2": "zero", "3": "zero"},
        ),
        (["--number", "123", "--name", "John"], {"number": "123", "name": "John"}),
        (
            ["--number", "123", "--name", "John", "--name", "Doe"],
            {"number": "123", "name": ["John", "Doe"]},
        ),
        (
            [
                "zero",
                "--number",
                "123",
                "one",
                "--name",
                "John",
                "--name",
                "Doe",
                "two",
            ],
            {
                "0": "zero",
                "number": "123",
                "name": ["John", "Doe"],
                "1": "one",
                "2": "two",
            },
        ),
    ],
)
def test_cli_args_all_extra_arguments_are_optional_and_schemaless(
    optional_args, expected
):
    actual = parse_cli_args(["some-tool", "some-env"] + optional_args)
    assert actual.tool is "some-tool"
    assert actual.env is "some-env"
    assert actual.extra_args == expected


@pytest.mark.parametrize(
    "args",
    [
        (["--help"]),
        (["-h"]),
    ],
)
def test_cli_args_should_show_help(args):
    actual = parse_cli_args(args)
    assert actual.show_help is True
    assert actual.tool is None
    assert actual.env is None

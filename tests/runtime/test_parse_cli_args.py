from typing import List, Set, Optional

import pytest
from pydantic import BaseModel

from hexagon.runtime.parse_args import parse_cli_args, should_support_multiple_args
from hexagon.support.input.args import PositionalArg, OptionalArg, ToolArgs


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
    assert actual.tool.value == expected
    assert actual.env is None
    assert actual.extra_args is None


def test_cli_args_tool_is_first_argument_2():
    actual = parse_cli_args(["some-env", "some-tool"])
    assert actual.tool.value == "some-env"
    assert actual.env.value == "some-tool"
    assert actual.extra_args is None


def test_cli_args_env_is_second_positional_argument():
    actual = parse_cli_args(["some-tool", "some-env"])
    assert actual.tool.value == "some-tool"
    assert actual.env.value == "some-env"
    assert actual.extra_args is None


@pytest.mark.parametrize(
    "optional_args,expected",
    [
        ([], None),
        (["--number", "123"], {"number": 123}),
        (["abc", "--number", "123"], {"0": "abc", "number": 123}),
        (["--number", "123", "abc"], {"0": "abc", "number": 123}),
        (
            ["zero", "one", "two", "three"],
            {"0": "zero", "1": "one", "2": "two", "3": "three"},
        ),
        (
            ["zero", "zero", "zero", "zero"],
            {"0": "zero", "1": "zero", "2": "zero", "3": "zero"},
        ),
        (["--number", "123", "--name", "John"], {"number": 123, "name": "John"}),
        (
            ["--name", "John", "--name", "Doe"],
            {"name": ["John", "Doe"]},
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
                "number": 123,
                "name": ["John", "Doe"],
                "1": "one",
                "2": "two",
            },
        ),
        (
            ["--foo", "bar", "--bar=baz", "--some", "--bass="],
            {
                "foo": "bar",
                "bar": "baz",
                "some": True,
                "bass": "",
            },
        ),
        (
            ["--foo"],
            {
                "foo": True,
            },
        ),
    ],
)
def test_cli_args_all_extra_arguments_mapping(optional_args, expected):
    actual = parse_cli_args(["some-tool", "some-env"] + optional_args)
    assert actual.tool.value == "some-tool"
    assert actual.env.value == "some-env"
    assert actual.extra_args == expected


def test_last_optional_arg_is_not_a_value():
    actual = parse_cli_args(["some-tool", "some-env", "--number"])
    assert actual.tool.value == "some-tool"
    assert actual.env.value == "some-env"
    assert actual.extra_args == {"number": True}


@pytest.mark.parametrize(
    "args,expected",
    [
        ([], []),
        (["some-tool"], ["some-tool"]),
        (["some-tool", "some-env"], ["some-tool", "some-env"]),
        (
            ["some-tool", "some-env", "--number=123"],
            ["some-tool", "some-env", "--number=123"],
        ),
        (["some-tool", "some-env", "abc"], ["some-tool", "some-env", "abc"]),
        (
            ["some-tool", "some-env", "--number", "123", "abc"],
            ["some-tool", "some-env", "--number", "123", "abc"],
        ),
        (
            ["some-tool", "some-env", "abc", "--number", "123"],
            ["some-tool", "some-env", "abc", "--number", "123"],
        ),
        (
            ["some-tool-group", "group-zero", "grou-one", "env", "--some-arg", "val"],
            ["some-tool-group", "group-zero", "grou-one", "env", "--some-arg", "val"],
        ),
    ],
)
def test_cli_args_as_list(args, expected):
    actual = parse_cli_args(args)
    assert actual.as_list() == expected


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


def test_get_generic_type_hint():
    class TestModel(BaseModel):
        name: PositionalArg[str] = None
        last_names: PositionalArg[List[str]] = None
        age: OptionalArg[int] = None
        friends: OptionalArg[List[int]] = None
        enemies: OptionalArg[Set[int]] = None
        relatives: OptionalArg[set] = None
        parents: OptionalArg[tuple] = None
        grand_parents: Optional[OptionalArg[tuple]] = None

    model = TestModel()

    assert should_support_multiple_args(model.__fields__["name"]) is False
    assert should_support_multiple_args(model.__fields__["last_names"]) is True
    assert should_support_multiple_args(model.__fields__["age"]) is False
    assert should_support_multiple_args(model.__fields__["friends"]) is True
    assert should_support_multiple_args(model.__fields__["enemies"]) is True
    assert should_support_multiple_args(model.__fields__["relatives"]) is True
    assert should_support_multiple_args(model.__fields__["parents"]) is True
    assert should_support_multiple_args(model.__fields__["grand_parents"]) is True


bool_input_keys = [
    "--proceed={val}",
    "--proceed {val}",
    "-p={val}",
    "-p {val}",
]

bool_input_values = [
    ("true", True),
    ("True", True),
    ("TRUE", True),
    ("on", True),
    ("On", True),
    ("ON", True),
    ("yes", True),
    ("Yes", True),
    ("YES", True),
    ("y", True),
    ("Y", True),
    ("1", True),
    ("false", False),
    ("False", False),
    ("FALSE", False),
    ("off", False),
    ("Off", False),
    ("OFF", False),
    ("no", False),
    ("No", False),
    ("NO", False),
    ("n", False),
    ("N", False),
    ("0", False),
]


@pytest.mark.parametrize(
    "cli_args,expected",
    [
        (["--proceed"], True),
        (["-p"], True),
        (["--no-proceed"], False),
        (["--no-p"], False),
    ]
    + [
        y
        for y in [
            (x.format(val=v).split(" "), e)
            for x in bool_input_keys
            for v, e in bool_input_values
        ]
    ],
)
def test_parse_tool_args_boolean(cli_args, expected):
    class Args(ToolArgs):
        proceed: OptionalArg[bool] = None

    actual = parse_cli_args(cli_args, Args)

    assert actual.proceed.value is expected
    assert actual.extra_args is None

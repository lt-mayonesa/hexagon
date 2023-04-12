from typing import List, Set, Optional

import pytest
from pydantic import BaseModel

from hexagon.domain.args import PositionalArg, OptionalArg
from hexagon.support.parse_args import parse_cli_args, should_support_multiple_args


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

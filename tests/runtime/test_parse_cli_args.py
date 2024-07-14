from enum import Enum
from typing import List, Set, Optional, Dict, Union, Any

import pytest
from pydantic import BaseModel

from hexagon.domain.hexagon_error import HexagonError
from hexagon.runtime.parse_args import parse_cli_args, should_support_multiple_args
from hexagon.support.input.args import PositionalArg, OptionalArg, ToolArgs
from hexagon.utils.typing import field_info


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
        (
            ["--float", "1.23"],
            {
                "float": 1.23,
            },
        ),
        (
            ["--bool", "true", "--not-bool", "false"],
            {"bool": True, "not-bool": False},
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


@pytest.mark.parametrize(
    "field,expected",
    [
        ("name", False),
        ("last_names", True),
        ("age", False),
        ("friends", True),
        ("enemies", True),
        ("relatives", True),
        ("parents", True),
        ("grand_parents", True),
    ],
)
def test_get_generic_type_hint(field, expected):
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

    assert should_support_multiple_args(model.model_fields[field]) is expected


class Country(str, Enum):
    BRAZIL = "Brazil"
    USA = "USA"
    CANADA = "Canada"


class Pet(BaseModel):
    name: str


@pytest.mark.parametrize(
    "field,expected_type,expected_iterable,expected_of_enum",
    [
        ("name", str, False, False),
        ("last_names", List[str], True, False),
        ("age", int, False, False),
        ("friends", List[int], True, False),
        ("enemies", Set[int], True, False),
        ("relatives", set, True, False),
        ("parents", tuple, True, False),
        ("grand_parents", tuple, True, False),
        ("great_grand_parents", tuple, True, False),
        ("country", Country, False, True),
        ("countries", List[Country], True, True),
        ("pets", Dict[str, Pet], False, False),
        ("random", int, False, False),
        ("random_list", List[int], True, False),
        ("nested", Dict[str, int], False, False),
    ],
)
def test_field_info(field, expected_type, expected_iterable, expected_of_enum):
    class TestModel(BaseModel):
        name: PositionalArg[str] = None
        last_names: PositionalArg[List[str]] = None
        age: OptionalArg[int] = None
        friends: OptionalArg[List[int]] = None
        enemies: OptionalArg[Set[int]] = None
        relatives: OptionalArg[set] = None
        parents: OptionalArg[tuple] = None
        grand_parents: Optional[OptionalArg[tuple]] = None
        great_grand_parents: OptionalArg[Optional[tuple]] = None
        country: OptionalArg[Country] = None
        countries: OptionalArg[List[Country]] = None
        pets: OptionalArg[Dict[str, Pet]] = None
        random: int = None
        random_list: List[int] = None
        nested: Optional[Dict[str, int]] = None

    model = TestModel()
    type_, iterable, of_enum = field_info(model.model_fields[field])

    assert type_ == expected_type
    assert iterable == expected_iterable
    assert of_enum == expected_of_enum


@pytest.mark.parametrize(
    "field",
    [
        "optional_arg_union",
        "arg_basic",
    ],
)
def test_field_with_multiple_types_should_raise_error(field):
    class TestModel(BaseModel):
        optional_arg_union: OptionalArg[Union[str, int]] = None
        arg_basic: Union[List[str], Dict[str, int], Any] = None

    model = TestModel()

    with pytest.raises(HexagonError):
        field_info(model.model_fields[field])


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

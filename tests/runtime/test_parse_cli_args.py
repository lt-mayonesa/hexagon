import pytest

from hexagon.runtime.parse_args import parse_cli_args
from hexagon.support.input.args import OptionalArg, ToolArgs


def test_parse_cli_args_returns_none_values_when_no_args_passed():
    """
    Given an empty list of command line arguments.
    When parse_cli_args is called with this empty list.
    Then the returned object should have tool=None, env=None, and extra_args=None.
    """
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
def test_parse_cli_args_sets_tool_value_when_only_tool_passed(args, expected):
    """
    Given command line arguments containing only a single value (e.g., ['some-tool']).
    When parse_cli_args is called with these arguments.
    Then the returned object should have tool.value equal to the provided argument.
    And env should be None.
    And extra_args should be None.
    """
    actual = parse_cli_args(args)
    assert actual.tool.value == expected
    assert actual.env is None
    assert actual.extra_args is None


def test_parse_cli_args_assigns_first_arg_to_tool_and_second_to_env():
    """
    Given command line arguments with two positional arguments ['some-env', 'some-tool'].
    When parse_cli_args is called with these arguments.
    Then the returned object should have tool.value='some-env' (first argument).
    And env.value='some-tool' (second argument).
    And extra_args should be None.
    """
    actual = parse_cli_args(["some-env", "some-tool"])
    assert actual.tool.value == "some-env"
    assert actual.env.value == "some-tool"
    assert actual.extra_args is None


def test_parse_cli_args_assigns_second_arg_to_env_when_tool_specified():
    """
    Given command line arguments ['some-tool', 'some-env'].
    When parse_cli_args is called with these arguments.
    Then the returned object should have tool.value='some-tool'.
    And env.value='some-env'.
    And extra_args should be None.
    """
    actual = parse_cli_args(["some-tool", "some-env"])
    assert actual.tool.value == "some-tool"
    assert actual.env.value == "some-env"
    assert actual.extra_args is None


def test_parse_cli_args_parses_named_arguments_with_equal_sign():
    """
    Given command line arguments ['some-tool', '--name=John', '--age=31', '--country=Argentina'].
    When parse_cli_args is called with these arguments.
    Then the returned object should have tool.value='some-tool'.
    And env should be None.
    And extra_args should be a dictionary with keys 'name', 'age', 'country'.
    And the values should be 'John', 31, and 'Argentina' respectively.
    """
    actual = parse_cli_args(
        [
            "some-tool",
            "--name=John",
            "--age=31",
            "--country=Argentina",
        ]
    )
    assert actual.tool.value == "some-tool"
    assert actual.env is None
    assert actual.extra_args == {
        "age": 31,
        "country": "Argentina",
        "name": "John",
    }


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
def test_parse_cli_args_maps_extra_arguments_correctly(optional_args, expected):
    """
    Given command line arguments with 'some-tool', 'some-env', and various extra arguments
    When parse_cli_args is called with these arguments
    Then the returned object should have tool.value='some-tool' and env.value='some-env'
    And extra_args should be mapped to a dictionary matching the expected structure for each test case
    """
    actual = parse_cli_args(["some-tool", "some-env"] + optional_args)
    assert actual.tool.value == "some-tool"
    assert actual.env.value == "some-env"
    assert actual.extra_args == expected


def test_parse_cli_args_treats_last_flag_as_boolean_when_no_value_provided():
    """
    Given command line arguments ['some-tool', 'some-env', '--number']
    When parse_cli_args is called with these arguments
    Then the returned object should have tool.value='some-tool' and env.value='some-env'
    And extra_args should be a dictionary with key 'number' and value True
    """
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
def test_parse_cli_args_returns_original_args_list_when_as_list_called(args, expected):
    """
    Given various command line arguments (e.g., ['some-tool', 'some-env', '--number', '123']).
    When parse_cli_args is called with these arguments and as_list() is called on the result.
    Then the exact same list of arguments that was passed in should be returned.
    """
    actual = parse_cli_args(args)
    assert actual.as_list() == expected


@pytest.mark.parametrize(
    "args",
    [
        (["--help"]),
        (["-h"]),
    ],
)
def test_parse_cli_args_sets_show_help_flag_when_help_option_provided(args):
    """
    Given command line arguments containing only a help option (e.g., ['--help'] or ['-h']).
    When parse_cli_args is called with these arguments.
    Then the returned object should have show_help=True.
    And tool=None, env=None, and extra_args=None.
    """
    actual = parse_cli_args(args)
    assert actual.show_help is True
    assert actual.tool is None
    assert actual.env is None


@pytest.mark.parametrize(
    "args",
    [
        (["--version"]),
        (["-v"]),
    ],
)
def test_parse_cli_args_sets_show_version_flag_when_version_option_provided(args):
    """
    Given command line arguments containing only a version option (e.g., ['--version'] or ['-v']).
    When parse_cli_args is called with these arguments.
    Then the returned object should have show_version=True.
    And show_help=False.
    And tool=None, env=None, and extra_args=None.
    """
    actual = parse_cli_args(args)
    assert actual.show_help is False
    assert actual.show_version is True
    assert actual.tool is None
    assert actual.env is None


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
def test_parse_cli_args_handles_boolean_flags_correctly(cli_args, expected):
    """
    Given command line arguments with boolean flags in various formats (e.g., '--proceed', '-p', '--proceed=true').
    When parse_cli_args is called with these arguments and a ToolArgs class that has a boolean field 'proceed'.
    Then the returned object should have proceed.value equal to the expected boolean value (True or False).
    And extra_args should be None.
    """

    class Args(ToolArgs):
        proceed: OptionalArg[bool] = None

    actual = parse_cli_args(cli_args, Args)

    assert actual.proceed.value is expected
    assert actual.extra_args is None

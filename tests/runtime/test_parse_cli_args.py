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


def test_parse_cli_args_handles_string_with_spaces_using_space_separator():
    """
    Given command line arguments with a space-separated optional string argument containing spaces.
    When parse_cli_args is called with ['--query', 'SELECT * FROM table'].
    Then query.value should equal the full string 'SELECT * FROM table'.
    """

    class Args(ToolArgs):
        query: OptionalArg[str] = None

    actual = parse_cli_args(["--query", "SELECT * FROM table"], Args)

    assert actual.query.value == "SELECT * FROM table"
    assert actual.extra_args is None


def test_parse_cli_args_handles_string_with_spaces_using_equals_separator():
    """
    Given command line arguments with an equals-separated optional string argument containing spaces.
    When parse_cli_args is called with ['--query=SELECT * FROM table'].
    Then query.value should equal the full string 'SELECT * FROM table'.
    """

    class Args(ToolArgs):
        query: OptionalArg[str] = None

    actual = parse_cli_args(["--query=SELECT * FROM table"], Args)

    assert actual.query.value == "SELECT * FROM table"
    assert actual.extra_args is None


@pytest.mark.parametrize(
    "cli_args,expected_query",
    [
        (["--query", ""], ""),
        (["--query", "  spaced  "], "  spaced  "),
        (["--query", "a  b  c"], "a  b  c"),
        (
            ["--query", "SELECT * FROM table WHERE name='O''Brien'"],
            "SELECT * FROM table WHERE name='O''Brien'",
        ),
        (["--query", "line1\nline2"], "line1\nline2"),
    ],
)
def test_parse_cli_args_handles_string_edge_cases(cli_args, expected_query):
    """
    Given command line arguments with edge case string values.
    When parse_cli_args is called with an OptionalArg[str] parameter.
    Then the full string value should be preserved exactly as provided.
    """

    class Args(ToolArgs):
        query: OptionalArg[str] = None

    actual = parse_cli_args(cli_args, Args)

    assert actual.query.value == expected_query
    assert actual.extra_args is None


def test_parse_cli_args_correctly_handles_env_after_unknown_option():
    """
    Given command line arguments ['some-tool', '--query', 'SELECT * FROM table', 'dev'].
    When parse_cli_args is called with CliArgs first.
    Then tool.value should be 'some-tool'.
    And raw_extra_args should contain ['--query', 'SELECT * FROM table', 'dev'].
    And the 'SELECT * FROM table' value should not be incorrectly consumed as env.
    """
    actual = parse_cli_args(["some-tool", "--query", "SELECT * FROM table", "dev"])

    assert actual.tool.value == "some-tool"
    assert actual.env is None
    assert "--query" in actual.raw_extra_args
    assert "SELECT * FROM table" in actual.raw_extra_args
    assert "dev" in actual.raw_extra_args


def test_parse_cli_args_handles_equals_in_value_with_equals_separator():
    """
    Given command line arguments with equals-separated value containing equals signs.
    When parse_cli_args is called with ['--query=SELECT * FROM t WHERE x = y'].
    Then query.value should equal the full string including the equals signs.
    """

    class Args(ToolArgs):
        query: OptionalArg[str] = None

    actual = parse_cli_args(["--query=SELECT * FROM t WHERE x = y"], Args)

    assert actual.query.value == "SELECT * FROM t WHERE x = y"
    assert actual.extra_args is None


def test_parse_cli_args_handles_complex_sql_query_with_multiple_equals_and_quotes():
    """
    Given command line arguments with a complex SQL query containing multiple equals signs, quotes, and special characters.
    When parse_cli_args is called with a real-world SQL query.
    Then the entire query should be preserved exactly as provided.
    """

    class Args(ToolArgs):
        query: OptionalArg[str] = None

    complex_query = (
        "SELECT COUNT(DISTINCT u.email) as active_users, "
        "SUM(p.amount) as total_revenue, "
        "STRING_AGG(DISTINCT u.country, ', ' ORDER BY u.country) as countries "
        "FROM users u "
        "JOIN purchases p ON u.id = p.user_id "
        "WHERE u.status = 'active' AND p.amount > 100 AND p.created_at >= '2024-01-01';"
    )

    actual = parse_cli_args([f"--query={complex_query}"], Args)

    assert actual.query.value == complex_query
    assert actual.extra_args is None


def test_parse_cli_args_handles_unix_paths_with_spaces():
    """
    Given command line arguments with Unix file path containing spaces.
    When parse_cli_args is called with ['--path=/home/user/My Documents/file.txt'].
    Then path.value should equal the full path exactly as provided.
    """

    class Args(ToolArgs):
        path: OptionalArg[str] = None

    actual = parse_cli_args(["--path=/home/user/My Documents/file.txt"], Args)

    assert actual.path.value == "/home/user/My Documents/file.txt"
    assert actual.extra_args is None


def test_parse_cli_args_handles_windows_paths_with_backslashes():
    """
    Given command line arguments with Windows file path containing backslashes.
    When parse_cli_args is called with ['--path=C:\\Users\\name\\Documents\\file.txt'].
    Then path.value should equal the full Windows path exactly as provided.
    """

    class Args(ToolArgs):
        path: OptionalArg[str] = None

    actual = parse_cli_args(["--path=C:\\Users\\name\\Documents\\file.txt"], Args)

    assert actual.path.value == "C:\\Users\\name\\Documents\\file.txt"
    assert actual.extra_args is None


def test_parse_cli_args_handles_relative_paths():
    """
    Given command line arguments with relative file path.
    When parse_cli_args is called with ['--path=../../some/path/to/file.txt'].
    Then path.value should equal the full relative path exactly as provided.
    """

    class Args(ToolArgs):
        path: OptionalArg[str] = None

    actual = parse_cli_args(["--path=../../some/path/to/file.txt"], Args)

    assert actual.path.value == "../../some/path/to/file.txt"
    assert actual.extra_args is None


def test_parse_cli_args_handles_tilde_expansion_paths():
    """
    Given command line arguments with tilde in file path.
    When parse_cli_args is called with ['--path=~/project/src/main.py'].
    Then path.value should equal the path with tilde exactly as provided.
    """

    class Args(ToolArgs):
        path: OptionalArg[str] = None

    actual = parse_cli_args(["--path=~/project/src/main.py"], Args)

    assert actual.path.value == "~/project/src/main.py"
    assert actual.extra_args is None


def test_parse_cli_args_handles_network_paths():
    """
    Given command line arguments with network file path (UNC path).
    When parse_cli_args is called with ['--path=\\\\server\\share\\file.txt'].
    Then path.value should equal the full network path exactly as provided.
    """

    class Args(ToolArgs):
        path: OptionalArg[str] = None

    actual = parse_cli_args(["--path=\\\\server\\share\\file.txt"], Args)

    assert actual.path.value == "\\\\server\\share\\file.txt"
    assert actual.extra_args is None


def test_parse_cli_args_handles_urls_with_query_params():
    """
    Given command line arguments with URL containing query parameters.
    When parse_cli_args is called with ['--url=https://api.example.com/v1/users?page=1&limit=10'].
    Then url.value should equal the full URL exactly as provided.
    """

    class Args(ToolArgs):
        url: OptionalArg[str] = None

    actual = parse_cli_args(
        ["--url=https://api.example.com/v1/users?page=1&limit=10"], Args
    )

    assert actual.url.value == "https://api.example.com/v1/users?page=1&limit=10"
    assert actual.extra_args is None


def test_parse_cli_args_handles_urls_with_auth_and_port():
    """
    Given command line arguments with URL containing authentication and port.
    When parse_cli_args is called with ['--url=https://user:pass@example.com:8080/api'].
    Then url.value should equal the full URL with auth and port exactly as provided.
    """

    class Args(ToolArgs):
        url: OptionalArg[str] = None

    actual = parse_cli_args(["--url=https://user:pass@example.com:8080/api"], Args)

    assert actual.url.value == "https://user:pass@example.com:8080/api"
    assert actual.extra_args is None


def test_parse_cli_args_handles_urls_with_fragments():
    """
    Given command line arguments with URL containing fragment identifier.
    When parse_cli_args is called with ['--url=https://docs.example.com/guide#installation'].
    Then url.value should equal the full URL with fragment exactly as provided.
    """

    class Args(ToolArgs):
        url: OptionalArg[str] = None

    actual = parse_cli_args(["--url=https://docs.example.com/guide#installation"], Args)

    assert actual.url.value == "https://docs.example.com/guide#installation"
    assert actual.extra_args is None


def test_parse_cli_args_handles_urls_with_encoded_chars():
    """
    Given command line arguments with URL containing encoded characters.
    When parse_cli_args is called with ['--url=https://example.com/search?q=hello%20world'].
    Then url.value should equal the full URL with encoded chars exactly as provided.
    """

    class Args(ToolArgs):
        url: OptionalArg[str] = None

    actual = parse_cli_args(["--url=https://example.com/search?q=hello%20world"], Args)

    assert actual.url.value == "https://example.com/search?q=hello%20world"
    assert actual.extra_args is None


def test_parse_cli_args_handles_urls_with_multiple_equals_in_query():
    """
    Given command line arguments with URL containing equals signs in query parameters.
    When parse_cli_args is called with ['--url=https://api.com?filter=status=active&sort=date'].
    Then url.value should equal the full URL with all equals signs exactly as provided.
    """

    class Args(ToolArgs):
        url: OptionalArg[str] = None

    actual = parse_cli_args(
        ["--url=https://api.com?filter=status=active&sort=date"], Args
    )

    assert actual.url.value == "https://api.com?filter=status=active&sort=date"
    assert actual.extra_args is None


def test_parse_cli_args_handles_negative_numbers():
    """
    Given command line arguments with negative number values.
    When parse_cli_args is called with ['--port=-1234'].
    Then port.value should equal -1234 as an integer.
    """

    class Args(ToolArgs):
        port: OptionalArg[int] = None

    actual = parse_cli_args(["--port=-1234"], Args)

    assert actual.port.value == -1234
    assert actual.extra_args is None


def test_parse_cli_args_handles_values_that_look_like_flags():
    """
    Given command line arguments with values that look like flags.
    When parse_cli_args is called with ['--message=--some-text'].
    Then message.value should equal '--some-text' as a string.
    """

    class Args(ToolArgs):
        message: OptionalArg[str] = None

    actual = parse_cli_args(["--message=--some-text"], Args)

    assert actual.message.value == "--some-text"
    assert actual.extra_args is None


def test_parse_cli_args_handles_whitespace_only_strings():
    """
    Given command line arguments with whitespace-only value.
    When parse_cli_args is called with ['--message=   '].
    Then message.value should equal the whitespace string exactly as provided.
    """

    class Args(ToolArgs):
        message: OptionalArg[str] = None

    actual = parse_cli_args(["--message=   "], Args)

    assert actual.message.value == "   "
    assert actual.extra_args is None


def test_parse_cli_args_handles_very_long_strings():
    """
    Given command line arguments with very long string value (10KB+).
    When parse_cli_args is called with a string exceeding 10,000 characters.
    Then the full string should be preserved exactly as provided.
    """

    class Args(ToolArgs):
        data: OptionalArg[str] = None

    long_string = "x" * 15000

    actual = parse_cli_args([f"--data={long_string}"], Args)

    assert actual.data.value == long_string
    assert len(actual.data.value) == 15000
    assert actual.extra_args is None


def test_parse_cli_args_handles_special_shell_characters():
    """
    Given command line arguments with special shell characters.
    When parse_cli_args is called with ['--cmd=ls -la | grep test'].
    Then cmd.value should equal the string with pipes and special chars exactly as provided.
    """

    class Args(ToolArgs):
        cmd: OptionalArg[str] = None

    actual = parse_cli_args(["--cmd=ls -la | grep test"], Args)

    assert actual.cmd.value == "ls -la | grep test"
    assert actual.extra_args is None


def test_parse_cli_args_handles_tab_and_newline_characters():
    """
    Given command line arguments with tab and newline characters.
    When parse_cli_args is called with string containing tabs and newlines.
    Then the tab and newline characters should be preserved exactly.
    """

    class Args(ToolArgs):
        text: OptionalArg[str] = None

    actual = parse_cli_args(["--text=line1\tcolumn2\nline2\tcolumn2"], Args)

    assert actual.text.value == "line1\tcolumn2\nline2\tcolumn2"
    assert actual.extra_args is None

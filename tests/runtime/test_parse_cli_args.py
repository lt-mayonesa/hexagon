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


def test_parse_cli_args_handles_json_inline():
    """
    Given command line arguments with inline JSON object.
    When parse_cli_args is called with ['--data={"key": "value", "nested": {"count": 10}}'].
    Then data.value should equal the full JSON string exactly as provided.
    """

    class Args(ToolArgs):
        data: OptionalArg[str] = None

    json_data = '{"key": "value", "nested": {"count": 10}}'

    actual = parse_cli_args([f"--data={json_data}"], Args)

    assert actual.data.value == json_data
    assert actual.extra_args is None


def test_parse_cli_args_handles_json_arrays():
    """
    Given command line arguments with JSON array.
    When parse_cli_args is called with ['--items=["item1", "item2", "item3"]'].
    Then items.value should equal the full JSON array exactly as provided.
    """

    class Args(ToolArgs):
        items: OptionalArg[str] = None

    json_array = '["item1", "item2", "item3"]'

    actual = parse_cli_args([f"--items={json_array}"], Args)

    assert actual.items.value == json_array
    assert actual.extra_args is None


def test_parse_cli_args_handles_json_with_escaped_quotes():
    """
    Given command line arguments with JSON containing escaped quotes.
    When parse_cli_args is called with JSON having quotes inside strings.
    Then the full JSON with escaped quotes should be preserved exactly.
    """

    class Args(ToolArgs):
        config: OptionalArg[str] = None

    json_config = '{"message": "Hello \\"World\\""}'

    actual = parse_cli_args([f"--config={json_config}"], Args)

    assert actual.config.value == json_config
    assert actual.extra_args is None


def test_parse_cli_args_handles_regex_patterns():
    """
    Given command line arguments with regex pattern.
    When parse_cli_args is called with ['--pattern=[a-z]+ \\d+'].
    Then pattern.value should equal the regex exactly as provided.
    """

    class Args(ToolArgs):
        pattern: OptionalArg[str] = None

    actual = parse_cli_args(["--pattern=[a-z]+ \\d+"], Args)

    assert actual.pattern.value == "[a-z]+ \\d+"
    assert actual.extra_args is None


def test_parse_cli_args_handles_complex_regex_with_groups():
    """
    Given command line arguments with complex regex pattern containing groups.
    When parse_cli_args is called with regex containing special characters and groups.
    Then the full regex pattern should be preserved exactly.
    """

    class Args(ToolArgs):
        pattern: OptionalArg[str] = None

    regex_pattern = "(?:https?:\\/\\/)?([\\w.-]+)"

    actual = parse_cli_args([f"--pattern={regex_pattern}"], Args)

    assert actual.pattern.value == regex_pattern
    assert actual.extra_args is None


def test_parse_cli_args_handles_email_validation_regex():
    """
    Given command line arguments with email validation regex.
    When parse_cli_args is called with complex email regex pattern.
    Then the full regex should be preserved with all special characters.
    """

    class Args(ToolArgs):
        pattern: OptionalArg[str] = None

    email_regex = "^\\w+@[\\w.-]+\\.[a-z]{2,}$"

    actual = parse_cli_args([f"--pattern={email_regex}"], Args)

    assert actual.pattern.value == email_regex
    assert actual.extra_args is None


def test_parse_cli_args_handles_shell_commands_with_pipes():
    """
    Given command line arguments with shell command containing pipes.
    When parse_cli_args is called with ['--cmd=ls -la | grep test | wc -l'].
    Then cmd.value should equal the full piped command exactly as provided.
    """

    class Args(ToolArgs):
        cmd: OptionalArg[str] = None

    actual = parse_cli_args(["--cmd=ls -la | grep test | wc -l"], Args)

    assert actual.cmd.value == "ls -la | grep test | wc -l"
    assert actual.extra_args is None


def test_parse_cli_args_handles_shell_commands_with_redirects():
    """
    Given command line arguments with shell command containing redirects.
    When parse_cli_args is called with command having output redirection.
    Then the full command with redirects should be preserved exactly.
    """

    class Args(ToolArgs):
        cmd: OptionalArg[str] = None

    shell_cmd = 'echo "data" > output.txt 2>&1'

    actual = parse_cli_args([f"--cmd={shell_cmd}"], Args)

    assert actual.cmd.value == shell_cmd
    assert actual.extra_args is None


def test_parse_cli_args_handles_shell_commands_with_chains():
    """
    Given command line arguments with chained shell commands.
    When parse_cli_args is called with ['--cmd=cd /tmp && ls && pwd'].
    Then cmd.value should equal the full command chain exactly as provided.
    """

    class Args(ToolArgs):
        cmd: OptionalArg[str] = None

    actual = parse_cli_args(["--cmd=cd /tmp && ls && pwd"], Args)

    assert actual.cmd.value == "cd /tmp && ls && pwd"
    assert actual.extra_args is None


def test_parse_cli_args_handles_markdown_text():
    """
    Given command line arguments with markdown formatted text.
    When parse_cli_args is called with markdown containing headers, bold, links.
    Then the full markdown should be preserved exactly.
    """

    class Args(ToolArgs):
        text: OptionalArg[str] = None

    markdown_text = "# Title\\n\\n**bold** text [link](url)"

    actual = parse_cli_args([f"--text={markdown_text}"], Args)

    assert actual.text.value == markdown_text
    assert actual.extra_args is None


def test_parse_cli_args_handles_html_tags():
    """
    Given command line arguments with HTML content.
    When parse_cli_args is called with ['--html=<div class="test">content</div>'].
    Then html.value should equal the HTML exactly as provided.
    """

    class Args(ToolArgs):
        html: OptionalArg[str] = None

    html_content = '<div class="test">content</div>'

    actual = parse_cli_args([f"--html={html_content}"], Args)

    assert actual.html.value == html_content
    assert actual.extra_args is None


def test_parse_cli_args_handles_xml_content():
    """
    Given command line arguments with XML content.
    When parse_cli_args is called with XML having attributes.
    Then the full XML should be preserved exactly.
    """

    class Args(ToolArgs):
        xml: OptionalArg[str] = None

    xml_content = '<tag attr="value">content</tag>'

    actual = parse_cli_args([f"--xml={xml_content}"], Args)

    assert actual.xml.value == xml_content
    assert actual.extra_args is None


def test_parse_cli_args_handles_environment_key_value_pairs():
    """
    Given command line arguments with environment-style key=value pairs.
    When parse_cli_args is called with ['--env=KEY1=val1 KEY2=val2'].
    Then env.value should equal the string with multiple equals signs exactly.
    """

    class Args(ToolArgs):
        env: OptionalArg[str] = None

    actual = parse_cli_args(["--env=KEY1=val1 KEY2=val2"], Args)

    assert actual.env.value == "KEY1=val1 KEY2=val2"
    assert actual.extra_args is None


def test_parse_cli_args_handles_database_connection_string():
    """
    Given command line arguments with database connection string containing equals signs.
    When parse_cli_args is called with DATABASE_URL style string.
    Then the full connection string should be preserved with all equals signs.
    """

    class Args(ToolArgs):
        db_url: OptionalArg[str] = None

    db_string = "DATABASE_URL=postgres://user:pass@host:5432/db?sslmode=require"

    actual = parse_cli_args([f"--db-url={db_string}"], Args)

    assert actual.db_url.value == db_string
    assert actual.extra_args is None


def test_parse_cli_args_handles_unicode_emoji_strings():
    """
    Given command line arguments with emoji characters.
    When parse_cli_args is called with ['--message=Hello 👋 World 🌍'].
    Then message.value should equal the string with emojis exactly as provided.
    """

    class Args(ToolArgs):
        message: OptionalArg[str] = None

    actual = parse_cli_args(["--message=Hello 👋 World 🌍"], Args)

    assert actual.message.value == "Hello 👋 World 🌍"
    assert actual.extra_args is None


def test_parse_cli_args_handles_cjk_characters():
    """
    Given command line arguments with Chinese/Japanese/Korean characters.
    When parse_cli_args is called with ['--text=你好世界'].
    Then text.value should equal the CJK string exactly as provided.
    """

    class Args(ToolArgs):
        text: OptionalArg[str] = None

    actual = parse_cli_args(["--text=你好世界"], Args)

    assert actual.text.value == "你好世界"
    assert actual.extra_args is None


def test_parse_cli_args_handles_arabic_rtl_text():
    """
    Given command line arguments with Arabic right-to-left text.
    When parse_cli_args is called with Arabic characters.
    Then the Arabic text should be preserved exactly.
    """

    class Args(ToolArgs):
        text: OptionalArg[str] = None

    actual = parse_cli_args(["--text=مرحبا بالعالم"], Args)

    assert actual.text.value == "مرحبا بالعالم"
    assert actual.extra_args is None


def test_parse_cli_args_handles_accented_characters():
    """
    Given command line arguments with accented European characters.
    When parse_cli_args is called with ['--text=Café résumé naïve'].
    Then text.value should equal the string with accents exactly as provided.
    """

    class Args(ToolArgs):
        text: OptionalArg[str] = None

    actual = parse_cli_args(["--text=Café résumé naïve"], Args)

    assert actual.text.value == "Café résumé naïve"
    assert actual.extra_args is None


def test_parse_cli_args_handles_multiple_complex_arguments_together():
    """
    Given command line arguments with multiple complex values simultaneously.
    When parse_cli_args is called with SQL query, URL, file path, and JSON together.
    Then all arguments should be parsed correctly and preserved exactly as provided.
    """

    class Args(ToolArgs):
        query: OptionalArg[str] = None
        url: OptionalArg[str] = None
        path: OptionalArg[str] = None
        config: OptionalArg[str] = None

    complex_query = "SELECT * FROM users WHERE email = 'test@example.com'"
    complex_url = "https://api.example.com/v1/data?filter=status=active&sort=date"
    complex_path = "/home/user/My Documents/project files/data.csv"
    complex_json = '{"key": "value", "nested": {"count": 10}}'

    actual = parse_cli_args(
        [
            f"--query={complex_query}",
            f"--url={complex_url}",
            f"--path={complex_path}",
            f"--config={complex_json}",
        ],
        Args,
    )

    assert actual.query.value == complex_query
    assert actual.url.value == complex_url
    assert actual.path.value == complex_path
    assert actual.config.value == complex_json
    assert actual.extra_args is None

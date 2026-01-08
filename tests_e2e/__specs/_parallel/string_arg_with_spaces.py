from tests_e2e.framework.hexagon_spec import as_a_user


def test_string_argument_with_spaces_using_space_separator():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with a space-separated value containing spaces.
    Then the entire quoted string should be received as the argument value.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["test-string-arg", "--query", "SELECT * FROM table"])
        .then_output_should_be(
            ["query: SELECT * FROM table"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_string_argument_with_spaces_using_equals_separator():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with an equals-separated value containing spaces.
    Then the entire string should be received as the argument value.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["test-string-arg", "--query=SELECT * FROM table"])
        .then_output_should_be(
            ["query: SELECT * FROM table"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_string_argument_with_complex_sql_query():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with a complex SQL query containing equals signs, quotes, and special characters.
    Then the entire query should be received exactly as provided (validated by checking query contains key parts).
    """
    query = (
        "SELECT COUNT(DISTINCT u.email) as active_users, "
        "SUM(p.amount) as total_revenue, "
        "STRING_AGG(DISTINCT u.country, ', ' ORDER BY u.country) as countries "
        "FROM users u "
        "JOIN purchases p ON u.id = p.user_id "
        "WHERE u.status = 'active' AND p.amount > 100 AND p.created_at >= '2024-01-01';"
    )
    (
        as_a_user(__file__)
        .run_hexagon(["test-string-arg", f"--query={query}"])
        .then_output_should_be(
            ["query: SELECT COUNT(DISTINCT u.email) as active_users"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_string_argument_with_file_path_containing_spaces():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with a file path containing spaces.
    Then the entire path should be received exactly as provided.
    """
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "test-string-arg",
                "--query=/home/user/My Documents/project files/data.csv",
            ]
        )
        .then_output_should_be(
            ["query: /home/user/My Documents/project files/data.csv"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_string_argument_with_url_and_query_params():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with a URL containing query parameters with equals signs.
    Then the entire URL should be received exactly as provided.
    """
    url = "https://api.example.com/v1/data?filter=status=active&sort=date&limit=100"
    (
        as_a_user(__file__)
        .run_hexagon(["test-string-arg", f"--query={url}"])
        .then_output_should_be(
            ["query: https://api.example.com/v1/data?filter=status=active"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_string_argument_with_shell_command():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with a shell command containing pipes and special characters.
    Then the entire command should be received exactly as provided.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["test-string-arg", "--query=ls -la | grep test | wc -l"])
        .then_output_should_be(
            ["query: ls -la | grep test | wc -l"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_string_argument_with_json_data():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with inline JSON data.
    Then the entire JSON should be received exactly as provided.
    """
    json_data = '{"key": "value", "nested": {"count": 10}}'
    (
        as_a_user(__file__)
        .run_hexagon(["test-string-arg", f"--query={json_data}"])
        .then_output_should_be(
            ['query: {"key": "value", "nested": {"count": 10}}'],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_string_argument_with_unicode_emoji():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with unicode emoji characters.
    Then the emoji characters should be received exactly as provided.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["test-string-arg", "--query=Hello 👋 World 🌍"])
        .then_output_should_be(
            ["query: Hello 👋 World 🌍"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_string_argument_with_cjk_characters():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with Chinese/Japanese/Korean characters.
    Then the CJK characters should be received exactly as provided.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["test-string-arg", "--query=你好世界"])
        .then_output_should_be(
            ["query: 你好世界"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_string_argument_with_regex_pattern():
    """
    Given a tool with an OptionalArg[str] parameter.
    When the user runs the tool with a regex pattern containing special characters.
    Then the regex pattern should be received exactly as provided.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["test-string-arg", r"--query=^\d{3}-\d{2}-\d{4}$"])
        .then_output_should_be(
            [r"query: ^\d{3}-\d{2}-\d{4}$"],
            discard_until_first_match=True,
        )
        .exit()
    )

from tests_e2e.framework.hexagon_spec import as_a_user


def test_multiple_complex_arguments_sql_url_path_json():
    """
    Given a tool with multiple OptionalArg[str] parameters.
    When the user runs the tool with SQL query, URL, file path, and JSON config together.
    Then all arguments should be received correctly and preserved exactly as provided.
    """
    query = "SELECT * FROM users WHERE email = 'test@example.com' AND status = 'active'"
    url = "https://api.example.com/v1/data?filter=status=active&sort=date"
    path = "/home/user/My Documents/project files/data.csv"
    config = '{"key": "value", "nested": {"count": 10}}'

    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "test-multiple-args",
                f"--query={query}",
                f"--url={url}",
                f"--path={path}",
                f"--config={config}",
            ]
        )
        .then_output_should_be(
            [
                "query: SELECT * FROM users WHERE email = 'test@example.com'",
                "url: https://api.example.com/v1/data?filter=status=active",
                "path: /home/user/My Documents/project files/data.csv",
                'config: {"key": "value", "nested": {"count": 10}}',
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_multiple_complex_arguments_with_unicode_and_special_chars():
    """
    Given a tool with multiple OptionalArg[str] parameters.
    When the user runs the tool with unicode, shell commands, regex, and HTML together.
    Then all arguments should be received correctly with all special characters preserved.
    """
    query = "Hello 👋 World 🌍 你好"
    url = "ls -la | grep test | wc -l"
    path = r"^\d{3}-\d{2}-\d{4}$"
    config = '<div class="test">content</div>'

    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "test-multiple-args",
                f"--query={query}",
                f"--url={url}",
                f"--path={path}",
                f"--config={config}",
            ]
        )
        .then_output_should_be(
            [
                "query: Hello 👋 World 🌍 你好",
                "url: ls -la | grep test | wc -l",
                r"path: ^\d{3}-\d{2}-\d{4}$",
                'config: <div class="test">content</div>',
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

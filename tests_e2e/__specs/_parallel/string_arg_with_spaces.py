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

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

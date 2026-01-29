from tests_e2e.framework.hexagon_spec import as_a_user


def test_tree_view_is_default_when_no_option_specified():
    """
    Given a CLI configuration without tool_display_mode option.
    When running the CLI.
    Then it should use tree view (current behavior).
    And tools from groups should NOT be visible in the main menu.
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                # Count: backup, database (group), plus 4 default tools = 6
                "6/6",
                "ƒ Backup Database",
                "≡ Database Tools",
                "⬡ Save Last Command as Shell Alias",
                "⬡ Replay Last Command",
                "⬡ Create A New Tool",
            ]
        )
        .exit()
    )


def test_tree_view_requires_navigation_into_groups():
    """
    Given a CLI configuration with tree view (default).
    When I want to access a tool inside a group.
    Then I must first navigate into that group.
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "6/6",
            ]
        )
        # Select the database group
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "2/2",  # migrate, go back
                "ƒ Run Migrations",
                "Go back",
            ]
        )
        .exit()
    )


def test_tree_view_with_cli_args_works_same_as_before():
    """
    Given a CLI configuration with tree view (default).
    When using CLI arguments to execute a tool in a group.
    Then the behavior should be exactly the same as before.
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon("database", "migrate")
        .then_output_should_be(
            [
                "Running migrations",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

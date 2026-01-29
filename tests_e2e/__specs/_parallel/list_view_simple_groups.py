from tests_e2e.framework.hexagon_spec import as_a_user


def test_list_view_shows_all_tools_in_flat_list():
    """
    Given a CLI configured with list view mode.
    And the CLI has tools in multiple groups.
    When running the CLI without arguments.
    Then all tools should be visible in a single flat list.
    And tools from groups should show their group context.
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                # Count includes: backup, database (group), migrate, rollback,
                # monitoring (group), logs, plus 4 default tools
                "10/10",
                "ƒ Backup Database",
                "≡ Database Tools",
                ["ƒ Run Migrations", "[Database Tools]"],  # On same line
                ["ƒ Rollback Migrations", "[Database Tools]"],  # On same line
                "≡ Monitoring Tools",
                ["ƒ View Logs", "[Monitoring Tools]"],  # On same line
            ]
        )
        .enter()  # Select first tool to complete test
        .then_output_should_be(["Running backup"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_with_cli_args_navigates_to_group():
    """
    Given a CLI configured with list view mode.
    When I use CLI arguments to navigate to a group.
    Then I should see only that group's tools.
    And I should NOT see a "Go back" option (consistent with tree view).
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon(["database"])
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "2/2",  # migrate, rollback (no go back)
                "ƒ Run Migrations",
                "ƒ Rollback Migrations",
            ],
            discard_until_first_match=True,
        )
        .enter()  # Select first tool to finish the test
        .then_output_should_be(
            ["Running migrations"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_list_view_with_cli_args_executes_tool_directly():
    """
    Given a CLI configured with list view mode.
    When I use CLI arguments to execute a tool in a group.
    Then the tool should execute directly without showing menus.
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon(["database", "migrate"])
        .then_output_should_be(
            [
                "Running migrations",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

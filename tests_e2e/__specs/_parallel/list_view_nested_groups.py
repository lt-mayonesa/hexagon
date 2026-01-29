from tests_e2e.framework.hexagon_spec import as_a_user


def test_nested_groups_show_full_path_in_list_view():
    """
    Given a CLI configured with list view mode.
    And there are deeply nested groups.
    When viewing the flat list.
    Then tools from nested groups should show the complete group hierarchy.
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                # Count: ops (group), deploy, database (nested group), backup, restore, plus 4 defaults
                "9/9",
                "≡ Operations",
                "ƒ Deploy Application",
                "[Operations]",
                "≡ Database Operations",
                "[Operations]",
                "ƒ Backup Database",
                "[Operations → Database Operations]",
                "ƒ Restore Database",
                "[Operations → Database Operations]",
            ]
        )
        .exit()
    )


def test_nested_groups_direct_execution_from_list_view():
    """
    Given a CLI configured with list view mode.
    And there is a tool in a deeply nested group.
    When I select that tool from the flat list.
    Then it should execute immediately.
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "9/9",
            ]
        )
        # Navigate to "backup" tool (which is in ops → database)
        .arrow_down()  # ops group
        .arrow_down()  # deploy
        .arrow_down()  # database group
        .arrow_down()  # backup
        .enter()
        .then_output_should_be(
            [
                ["ƒ Backup Database", "[Operations → Database Operations]"],
                "Backing up database",
            ]
        )
        .exit()
    )


def test_nested_groups_navigation_with_cli_args():
    """
    Given a CLI configured with list view mode.
    And there are deeply nested groups.
    When I use CLI arguments to navigate through nested groups.
    Then the navigation should work exactly as in tree view.
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon("ops", "database", "backup")
        .then_output_should_be(
            [
                "Backing up database",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_nested_groups_can_navigate_into_parent_group():
    """
    Given a CLI configured with list view mode.
    And there is a parent group in the flat list.
    When I select that parent group.
    Then I should see its tools and nested groups in list view format.
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "8/8",
            ]
        )
        # Select the ops group
        .enter()  # ops is first
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                # deploy, database (nested group), backup, restore, go back
                "5/5",
                "ƒ Deploy Application",
                "≡ Database Operations",
                "ƒ Backup Database",
                "[Database Operations]",
                "ƒ Restore Database",
                "[Database Operations]",
                "Go back",
            ]
        )
        .exit()
    )

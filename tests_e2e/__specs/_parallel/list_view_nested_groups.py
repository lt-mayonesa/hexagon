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
                # Count: ops (group), deploy, database (nested group), backup, restore, plus 4 defaults = 9
                "9/9",
                "≡ Operations",
                ["ƒ Deploy Application", "[Operations]"],
                ["≡ Database Operations", "[Operations]"],
                ["ƒ Backup Database", "[Operations → Database Operations]"],
                ["ƒ Restore Database", "[Operations → Database Operations]"],
            ]
        )
        .arrow_down()  # Skip ops group
        .enter()  # Select deploy tool
        .then_output_should_be(
            ["Deploying application"], discard_until_first_match=True
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
        .run_hexagon(["ops", "database", "backup"])
        .then_output_should_be(
            [
                "Backing up database",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

from tests_e2e.framework.hexagon_spec import as_a_user


def test_flat_tool_display_shows_all_tools_in_single_list():
    """
    Given a CLI with tool_display_mode set to flat.
    When hexagon is run.
    Then all tools from groups are shown in a flat list with tool names first.
    """
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "15/15",  # 2 top-level + group1 + 3 from group1 + group2 + 1 from group2 + nested-group + 1 from nested + separator + 4 default
                "ƒ Tool 1",
                "ƒ Tool 2",
                "≡ Group 1",
                "ƒ Tool 3 [Group 1]",
                "⦾ Tool 4 [Group 1]",
                "≡ Group 2",
                "ƒ Tool 5 [Group 2]",
                "≡ Nested Group [Group 2]",
                "ƒ Tool 6 [Group 2 › Nested Group]",
            ],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["Tool 1"], discard_until_first_match=True)
        .exit()
    )


def test_flat_tool_display_can_execute_nested_tool():
    """
    Given a CLI with tool_display_mode set to list.
    When a tool from a nested group is selected.
    Then the tool executes correctly.
    """
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "15/15",
            ]
        )
        .arrow_down()  # Move to tool2
        .arrow_down()  # Move to group1
        .arrow_down()  # Move to tool3 [group1]
        .arrow_down()  # Move to tool4 [group1]
        .arrow_down()  # Move to tool-with-env [group1]
        .arrow_down()  # Move to separator
        .arrow_down()  # Move to group2
        .arrow_down()  # Move to tool5 [group2]
        .arrow_down()  # Move to nested-group [group2]
        .arrow_down()  # Move to tool6 [group2 › nested-group]
        .enter()
        .then_output_should_be(
            [
                "tool6",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_flat_tool_display_can_select_tool_by_name():
    """
    Given a CLI with tool_display_mode set to list.
    When a tool is selected using full path (same as tree view).
    Then the tool executes without showing the menu.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["group1", "tool3"])
        .then_output_should_be(
            [
                "tool3",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_flat_tool_display_can_navigate_into_group_via_cli():
    """
    Given a CLI with tool_display_mode set to list.
    When a group is selected via CLI args.
    Then only the group's tools are shown for selection.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["group1"])
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "3/3",  # tool3, tool4, tool-with-env
                "ƒ Tool 3",
                "⦾ Tool 4",
                "ƒ Tool With Env",
            ],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["tool3"], discard_until_first_match=True)
        .exit()
    )


def test_flat_tool_display_can_navigate_into_nested_group_via_cli():
    """
    Given a CLI with tool_display_mode set to list.
    When a nested group is selected via CLI args.
    Then only the nested group's tools are shown.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["group2", "nested-group"])
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "1/1",
                "ƒ Tool 6",
            ],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["tool6"], discard_until_first_match=True)
        .exit()
    )


def test_flat_tool_display_can_select_group_from_menu_then_tool():
    """
    Given a CLI with tool_display_mode set to list.
    When a group is selected from the interactive menu.
    Then the user can navigate into it and select a tool.
    """
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "15/15",
            ]
        )
        .arrow_down()  # Move to tool2
        .arrow_down()  # Move to group1
        .enter()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "4/4",  # 3 tools + go back
                "ƒ Tool 3",
                "⦾ Tool 4",
                "ƒ Tool With Env",
                "↩ Go back",
            ],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["tool3"], discard_until_first_match=True)
        .exit()
    )


def test_flat_tool_display_can_select_nested_group_from_menu_then_tool():
    """
    Given a CLI with tool_display_mode set to list.
    When navigating through groups to a nested group.
    Then the user can navigate into it and select a tool.
    """
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "15/15",
            ]
        )
        .arrow_down()  # Move to tool2
        .arrow_down()  # Move to group1
        .arrow_down()  # Move to tool3 [group1]
        .arrow_down()  # Move to tool4 [group1]
        .arrow_down()  # Move to tool-with-env [group1]
        .arrow_down()  # Move to separator
        .arrow_down()  # Move to group2
        .enter()  # Enter group2
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "4/4",  # tool5 + nested-group + tool6[nested-group] + go back
                "ƒ Tool 5",
                "≡ Nested Group",
                "ƒ Tool 6 [Nested Group]",
                "↩ Go back",
            ],
            discard_until_first_match=True,
        )
        .arrow_down()  # Move to nested-group
        .enter()  # Enter nested-group
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "2/2",  # tool6 + go back
                "ƒ Tool 6",
                "↩ Go back",
            ],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["tool6"], discard_until_first_match=True)
        .exit()
    )


def test_flat_tool_display_can_execute_tool_from_group_directly_in_flat_list():
    """
    Given a CLI with tool_display_mode set to list.
    When a tool with group context is selected from the flat list.
    Then it executes directly without entering the group.
    """
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "15/15",
            ]
        )
        .arrow_down()  # Move to tool2
        .arrow_down()  # Move to group1
        .arrow_down()  # Move to tool3 [group1]
        .enter()
        .then_output_should_be(["tool3"], discard_until_first_match=True)
        .exit()
    )


def test_flat_tool_display_can_execute_deeply_nested_tool_via_cli():
    """
    Given a CLI with tool_display_mode set to list.
    When a deeply nested tool is selected via full CLI path.
    Then it executes directly without showing any menus.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["group2", "nested-group", "tool6"])
        .then_output_should_be(["tool6"], discard_until_first_match=True)
        .exit()
    )

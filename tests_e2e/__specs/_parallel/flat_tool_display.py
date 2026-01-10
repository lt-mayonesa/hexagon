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
                "11/11",  # 6 tools + separator + 4 default tools
                "ƒ Tool 1",
                "ƒ Tool 2",
                "ƒ Tool 3 [group1]",
                "⦾ Tool 4 [group1]",
                "ƒ Tool 5 [group2]",
                "ƒ Tool 6 [group2 › nested-group]",
            ],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["Tool 1"], discard_until_first_match=True)
        .exit()
    )


def test_flat_tool_display_can_execute_nested_tool():
    """
    Given a CLI with tool_display_mode set to flat.
    When a tool from a nested group is selected.
    Then the tool executes correctly.
    """
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "11/11",
            ]
        )
        .arrow_down()  # Move to tool2
        .arrow_down()  # Move to tool3 [group1]
        .arrow_down()  # Move to tool4 [group1]
        .arrow_down()  # Move to separator
        .arrow_down()  # Move to tool5 [group2]
        .arrow_down()  # Move to tool6 [group2 › nested-group]
        .enter()
        .then_output_should_be(
            [
                "Tool 6 [group2 › nested-group]",
                "tool6",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_flat_tool_display_can_select_tool_by_name():
    """
    Given a CLI with tool_display_mode set to flat.
    When a tool is selected by name using CLI args.
    Then the tool executes without showing the menu.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["tool3"])
        .then_output_should_be(
            [
                "tool3",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

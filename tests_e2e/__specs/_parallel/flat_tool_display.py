from tests_e2e.framework.hexagon_spec import as_a_user


def test_flat_tool_display_shows_all_tools_in_single_list():
    """
    Given a CLI with flat_tool_display option enabled.
    When hexagon is run.
    Then all tools from groups are shown in a flat list with prefixed names.
    """
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "10/10",
                "ƒ Tool 1",
                "ƒ Tool 2",
                "ƒ group1 / Tool 3",
                "⦾ group1 / Tool 4",
                "ƒ group2 / nested-group / Tool 6",
            ],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["Tool 1"], discard_until_first_match=True)
        .exit()
    )


def test_flat_tool_display_can_execute_nested_tool():
    """
    Given a CLI with flat_tool_display option enabled.
    When a tool from a nested group is selected.
    Then the tool executes correctly.
    """
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "10/10",
            ]
        )
        .arrow_down()  # Move to tool2
        .arrow_down()  # Move to group1 / tool3
        .arrow_down()  # Move to group1 / tool4
        .arrow_down()  # Move to group2 / tool5
        .arrow_down()  # Move to group2 / nested-group / tool6
        .enter()
        .then_output_should_be(
            [
                "group2 / nested-group / Tool 6",
                "tool6",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_flat_tool_display_can_select_tool_by_name():
    """
    Given a CLI with flat_tool_display option enabled.
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

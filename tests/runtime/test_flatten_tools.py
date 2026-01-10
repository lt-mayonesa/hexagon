from hexagon.domain.tool import ActionTool, GroupTool, ToolType, Separator, FunctionTool
from hexagon.runtime.presentation.list_view import flatten_tools


def test_flatten_tools_no_groups():
    """
    Given a list of tools without any groups.
    When flatten_tools is called.
    Then it returns the same list of tools.
    """
    tools = [
        ActionTool(name="tool1", type=ToolType.misc, action="echo 1"),
        ActionTool(name="tool2", type=ToolType.shell, action="echo 2"),
    ]

    result = flatten_tools(tools)

    assert len(result) == 2
    assert result[0].name == "tool1"
    assert result[1].name == "tool2"


def test_flatten_tools_with_single_level_group():
    """
    Given a list of tools with one group containing nested tools.
    When flatten_tools is called.
    Then nested tools show tool name first with group context in brackets.
    And original names are preserved as aliases for CLI selection.
    """
    tools = [
        ActionTool(name="tool1", type=ToolType.misc, action="echo 1"),
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                ActionTool(name="tool2", type=ToolType.shell, action="echo 2"),
                ActionTool(name="tool3", type=ToolType.web, action="echo 3"),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 3  # tool1, tool2, tool3 (no separator after non-group tool)
    assert result[0].name == "tool1"
    assert result[1].name == "tool2 [group1]"
    assert result[1].alias == "tool2"  # Original name preserved as alias
    assert result[2].name == "tool3 [group1]"
    assert result[2].alias == "tool3"  # Original name preserved as alias


def test_flatten_tools_with_nested_groups():
    """
    Given a list of tools with nested groups (group within a group).
    When flatten_tools is called.
    Then nested tools show tool name with full group path in brackets.
    """
    tools = [
        ActionTool(name="tool1", type=ToolType.misc, action="echo 1"),
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                ActionTool(name="tool2", type=ToolType.shell, action="echo 2"),
                GroupTool(
                    name="group2",
                    type=ToolType.group,
                    tools=[
                        ActionTool(name="tool3", type=ToolType.web, action="echo 3"),
                        ActionTool(name="tool4", type=ToolType.misc, action="echo 4"),
                    ],
                ),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 4  # tool1, tool2, tool3, tool4 (no separators)
    assert result[0].name == "tool1"
    assert result[1].name == "tool2 [group1]"
    assert result[2].name == "tool3 [group1 › group2]"
    assert result[3].name == "tool4 [group1 › group2]"


def test_flatten_tools_preserves_long_name():
    """
    Given a tool with a long_name inside a group.
    When flatten_tools is called.
    Then the long_name also includes the group context.
    """
    tools = [
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                ActionTool(
                    name="tool1",
                    long_name="Tool One",
                    type=ToolType.shell,
                    action="echo 1",
                ),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 1
    assert result[0].name == "tool1 [group1]"
    assert result[0].long_name == "Tool One [group1]"


def test_flatten_tools_preserves_description():
    """
    Given a tool with a description inside a group.
    When flatten_tools is called.
    Then the description is preserved unchanged.
    """
    tools = [
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                ActionTool(
                    name="tool1",
                    description="A test tool",
                    type=ToolType.shell,
                    action="echo 1",
                ),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 1
    assert result[0].name == "tool1 [group1]"
    assert result[0].description == "A test tool"


def test_flatten_tools_multiple_groups_same_level():
    """
    Given multiple groups at the same level.
    When flatten_tools is called.
    Then tools from each group are properly formatted.
    And a separator is added between groups.
    """
    tools = [
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                ActionTool(name="tool1", type=ToolType.shell, action="echo 1"),
            ],
        ),
        GroupTool(
            name="group2",
            type=ToolType.group,
            tools=[
                ActionTool(name="tool2", type=ToolType.web, action="echo 2"),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 3  # tool1, separator, tool2
    assert result[0].name == "tool1 [group1]"
    assert result[1].type == ToolType.separator
    assert result[2].name == "tool2 [group2]"


def test_flatten_tools_preserves_existing_alias():
    """
    Given a tool with an existing alias inside a group.
    When flatten_tools is called.
    Then the existing alias is preserved and not overwritten.
    """
    tools = [
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                ActionTool(
                    name="tool1",
                    alias="t1",
                    type=ToolType.shell,
                    action="echo 1",
                ),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 1
    assert result[0].name == "tool1 [group1]"
    assert result[0].alias == "t1"


def test_flatten_tools_filters_separators_in_groups():
    """
    Given a group containing separators.
    When flatten_tools is called.
    Then separators inside groups are filtered out.
    And only top-level separators are preserved.
    """
    tools = [
        ActionTool(name="tool1", type=ToolType.misc, action="echo 1"),
        Separator,
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                ActionTool(name="tool2", type=ToolType.shell, action="echo 2"),
                Separator,  # This should be filtered out
                ActionTool(name="tool3", type=ToolType.web, action="echo 3"),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 4  # tool1, separator (top-level), tool2, tool3
    assert result[0].name == "tool1"
    assert result[1].type == ToolType.separator
    assert result[2].name == "tool2 [group1]"
    assert result[3].name == "tool3 [group1]"


def test_flatten_tools_handles_triple_nesting():
    """
    Given a deeply nested group structure (3+ levels).
    When flatten_tools is called.
    Then the full group path is shown in brackets.
    """
    tools = [
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                GroupTool(
                    name="group2",
                    type=ToolType.group,
                    tools=[
                        GroupTool(
                            name="group3",
                            type=ToolType.group,
                            tools=[
                                ActionTool(
                                    name="tool1", type=ToolType.shell, action="echo 1"
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 1  # just tool1, no separator for single group
    assert result[0].name == "tool1 [group1 › group2 › group3]"
    assert result[0].alias == "tool1"


def test_flatten_tools_handles_empty_groups():
    """
    Given a group with no tools.
    When flatten_tools is called.
    Then no tools or separators are added for that group.
    """
    tools = [
        ActionTool(name="tool1", type=ToolType.misc, action="echo 1"),
        GroupTool(
            name="empty-group",
            type=ToolType.group,
            tools=[],
        ),
        ActionTool(name="tool2", type=ToolType.misc, action="echo 2"),
    ]

    result = flatten_tools(tools)

    assert len(result) == 2
    assert result[0].name == "tool1"
    assert result[1].name == "tool2"


def test_flatten_tools_handles_group_with_only_separators():
    """
    Given a group containing only separators.
    When flatten_tools is called.
    Then the group contributes no tools to the flattened list.
    And no separator is added for the empty group.
    """
    tools = [
        ActionTool(name="tool1", type=ToolType.misc, action="echo 1"),
        GroupTool(
            name="separator-group",
            type=ToolType.group,
            tools=[Separator, Separator],
        ),
        ActionTool(name="tool2", type=ToolType.misc, action="echo 2"),
    ]

    result = flatten_tools(tools)

    assert len(result) == 2
    assert result[0].name == "tool1"
    assert result[1].name == "tool2"


def test_flatten_tools_preserves_function_tool():
    """
    Given a FunctionTool inside a group.
    When flatten_tools is called.
    Then the function reference is preserved (not serialized).
    """

    def dummy_function():
        return "test"

    tools = [
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                FunctionTool(
                    name="func-tool",
                    type=ToolType.function,
                    function=dummy_function,
                ),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 1
    assert result[0].name == "func-tool [group1]"
    assert isinstance(result[0], FunctionTool)
    assert result[0].function == dummy_function
    assert result[0].function() == "test"


def test_flatten_tools_preserves_icon():
    """
    Given a tool with an icon inside a group.
    When flatten_tools is called.
    Then the icon is preserved.
    """
    tools = [
        GroupTool(
            name="database",
            type=ToolType.group,
            icon="🗄️",
            tools=[
                ActionTool(
                    name="migrate",
                    icon="⚡",
                    type=ToolType.shell,
                    action="echo migrate",
                ),
            ],
        ),
    ]

    result = flatten_tools(tools)

    assert len(result) == 1
    assert result[0].name == "migrate [database]"
    assert result[0].icon == "⚡"

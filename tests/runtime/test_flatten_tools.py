from hexagon.domain.tool import (
    ActionTool,
    GroupTool,
    ToolType,
    Separator,
    FunctionTool,
    GroupPathItem,
)
from hexagon.runtime.presentation.list_view import list_view


def test_list_view_no_groups():
    """
    Given a list of tools without any groups.
    When list_view is called.
    Then it returns the same list of tools.
    And group_path is None for top-level tools.
    """
    tools = [
        ActionTool(name="tool1", type=ToolType.misc, action="echo 1"),
        ActionTool(name="tool2", type=ToolType.shell, action="echo 2"),
    ]

    result = list_view(tools)

    assert len(result) == 2
    assert result[0].name == "tool1"
    assert result[0].group_path is None
    assert result[1].name == "tool2"
    assert result[1].group_path is None


def test_list_view_with_single_level_group():
    """
    Given a list of tools with one group containing nested tools.
    When list_view is called.
    Then the group is included in the result for navigation.
    And nested tools show tool name first with group context in brackets.
    And group_path contains the parent group information.
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

    result = list_view(tools)

    assert len(result) == 4  # tool1 + group1 + tool2 + tool3
    assert result[0].name == "tool1"
    assert result[0].group_path is None
    assert result[1].name == "group1"
    assert result[1].type == ToolType.group
    assert result[2].name == "tool2"
    assert result[2].long_name == "tool2 [group1]"
    assert result[2].alias is None
    assert result[2].group_path == [GroupPathItem(name="group1", alias=None)]
    assert result[3].name == "tool3"
    assert result[3].long_name == "tool3 [group1]"
    assert result[3].alias is None
    assert result[3].group_path == [GroupPathItem(name="group1", alias=None)]


def test_list_view_with_nested_groups():
    """
    Given a list of tools with nested groups (group within a group).
    When list_view is called.
    Then both groups and their tools are included.
    And nested tools show tool name with full group path in brackets.
    And group_path contains all ancestor groups.
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

    result = list_view(tools)

    # tool1, group1, tool2, group2, tool3, tool4
    assert len(result) == 6
    assert result[0].name == "tool1"
    assert result[0].group_path is None
    assert result[1].name == "group1"
    assert result[1].type == ToolType.group
    assert result[2].name == "tool2"
    assert result[2].long_name == "tool2 [group1]"
    assert result[2].group_path == [GroupPathItem(name="group1", alias=None)]
    assert result[3].name == "group2"
    assert result[3].long_name == "group2 [group1]"
    assert result[3].group_path == [GroupPathItem(name="group1", alias=None)]
    assert result[4].name == "tool3"
    assert result[4].long_name == "tool3 [group1 › group2]"
    assert result[4].group_path == [
        GroupPathItem(name="group1", alias=None),
        GroupPathItem(name="group2", alias=None),
    ]
    assert result[5].name == "tool4"
    assert result[5].long_name == "tool4 [group1 › group2]"
    assert result[5].group_path == [
        GroupPathItem(name="group1", alias=None),
        GroupPathItem(name="group2", alias=None),
    ]


def test_list_view_preserves_long_name():
    """
    Given a tool with a long_name inside a group.
    When list_view is called.
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

    result = list_view(tools)

    assert len(result) == 2  # group1 + tool1
    assert result[0].name == "group1"
    assert result[1].name == "tool1"
    assert result[1].long_name == "Tool One [group1]"


def test_list_view_preserves_description():
    """
    Given a tool with a description inside a group.
    When list_view is called.
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

    result = list_view(tools)

    assert len(result) == 2  # group1 + tool1
    assert result[0].name == "group1"
    assert result[1].name == "tool1"
    assert result[1].long_name == "tool1 [group1]"
    assert result[1].description == "A test tool"


def test_list_view_multiple_groups_same_level():
    """
    Given multiple groups at the same level.
    When list_view is called.
    Then groups and tools from each group are included.
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

    result = list_view(tools)

    # group1, tool1, separator, group2, tool2
    assert len(result) == 5
    assert result[0].name == "group1"
    assert result[1].name == "tool1"
    assert result[1].long_name == "tool1 [group1]"
    assert result[2].type == ToolType.separator
    assert result[3].name == "group2"
    assert result[4].name == "tool2"
    assert result[4].long_name == "tool2 [group2]"


def test_list_view_preserves_existing_alias():
    """
    Given a tool with an existing alias inside a group.
    When list_view is called.
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

    result = list_view(tools)

    assert len(result) == 2  # group1 + tool1
    assert result[0].name == "group1"
    assert result[1].name == "tool1"
    assert result[1].long_name == "tool1 [group1]"
    assert result[1].alias == "t1"


def test_list_view_filters_separators_in_groups():
    """
    Given a group containing separators.
    When list_view is called.
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

    result = list_view(tools)

    # tool1, separator, group1, tool2, tool3
    assert len(result) == 5
    assert result[0].name == "tool1"
    assert result[1].type == ToolType.separator
    assert result[2].name == "group1"
    assert result[3].name == "tool2"
    assert result[3].long_name == "tool2 [group1]"
    assert result[4].name == "tool3"
    assert result[4].long_name == "tool3 [group1]"


def test_list_view_handles_triple_nesting():
    """
    Given a deeply nested group structure (3+ levels).
    When list_view is called.
    Then all groups and the tool are included.
    And the full group path is shown in brackets for the tool.
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

    result = list_view(tools)

    # group1, group2, group3, tool1
    assert len(result) == 4
    assert result[0].name == "group1"
    assert result[1].name == "group2"
    assert result[1].long_name == "group2 [group1]"
    assert result[2].name == "group3"
    assert result[2].long_name == "group3 [group1 › group2]"
    assert result[3].name == "tool1"
    assert result[3].long_name == "tool1 [group1 › group2 › group3]"
    assert result[3].alias is None


def test_list_view_handles_empty_groups():
    """
    Given a group with no tools.
    When list_view is called.
    Then the empty group is still included (for consistency).
    But it contributes no child tools.
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

    result = list_view(tools)

    # tool1, empty-group, tool2
    assert len(result) == 3
    assert result[0].name == "tool1"
    assert result[1].name == "empty-group"
    assert result[1].type == ToolType.group
    assert result[2].name == "tool2"


def test_list_view_handles_group_with_only_separators():
    """
    Given a group containing only separators.
    When list_view is called.
    Then the group is included but contributes no tools.
    And separators inside groups are filtered out.
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

    result = list_view(tools)

    # tool1, separator-group, tool2
    assert len(result) == 3
    assert result[0].name == "tool1"
    assert result[1].name == "separator-group"
    assert result[1].type == ToolType.group
    assert result[2].name == "tool2"


def test_list_view_preserves_function_tool():
    """
    Given a FunctionTool inside a group.
    When list_view is called.
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

    result = list_view(tools)

    assert len(result) == 2  # group1 + func-tool
    assert result[0].name == "group1"
    assert result[1].name == "func-tool"
    assert result[1].long_name == "func-tool [group1]"
    assert isinstance(result[1], FunctionTool)
    assert result[1].function == dummy_function
    assert result[1].function() == "test"


def test_list_view_preserves_icon():
    """
    Given a tool with an icon inside a group.
    When list_view is called.
    Then the icon is preserved.
    And group_path is populated.
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

    result = list_view(tools)

    assert len(result) == 2  # database + migrate
    assert result[0].name == "database"
    assert result[0].icon == "🗄️"
    assert result[1].name == "migrate"
    assert result[1].long_name == "migrate [database]"
    assert result[1].icon == "⚡"
    assert result[1].group_path == [GroupPathItem(name="database", alias=None)]


def test_list_view_captures_group_aliases_in_path():
    """
    Given groups with aliases.
    When list_view is called.
    Then group_path includes the aliases.
    """
    tools = [
        GroupTool(
            name="tool-group",
            alias="tg",
            type=ToolType.group,
            tools=[
                ActionTool(
                    name="group-command",
                    alias="gc",
                    type=ToolType.shell,
                    action="echo test",
                ),
            ],
        ),
    ]

    result = list_view(tools)

    assert len(result) == 2  # tool-group + group-command
    assert result[0].name == "tool-group"
    assert result[0].alias == "tg"
    assert result[1].name == "group-command"
    assert result[1].alias == "gc"
    assert result[1].group_path == [GroupPathItem(name="tool-group", alias="tg")]

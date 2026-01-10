from hexagon.domain.tool import ActionTool, GroupTool, ToolType
from hexagon.runtime.configuration import flatten_tools


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
    Then nested tools are prefixed with the group name.
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

    assert len(result) == 3
    assert result[0].name == "tool1"
    assert result[1].name == "group1 / tool2"
    assert result[1].alias == "tool2"  # Original name preserved as alias
    assert result[2].name == "group1 / tool3"
    assert result[2].alias == "tool3"  # Original name preserved as alias


def test_flatten_tools_with_nested_groups():
    """
    Given a list of tools with nested groups (group within a group).
    When flatten_tools is called.
    Then nested tools are prefixed with full path.
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

    assert len(result) == 4
    assert result[0].name == "tool1"
    assert result[1].name == "group1 / tool2"
    assert result[2].name == "group1 / group2 / tool3"
    assert result[3].name == "group1 / group2 / tool4"


def test_flatten_tools_preserves_long_name():
    """
    Given a tool with a long_name inside a group.
    When flatten_tools is called.
    Then the long_name is also prefixed with the group name.
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
    assert result[0].name == "group1 / tool1"
    assert result[0].long_name == "group1 / Tool One"


def test_flatten_tools_preserves_description():
    """
    Given a tool with a description inside a group.
    When flatten_tools is called.
    Then the description is preserved.
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
    assert result[0].name == "group1 / tool1"
    assert result[0].description == "A test tool"


def test_flatten_tools_multiple_groups_same_level():
    """
    Given multiple groups at the same level.
    When flatten_tools is called.
    Then tools from each group are properly prefixed.
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

    assert len(result) == 2
    assert result[0].name == "group1 / tool1"
    assert result[1].name == "group2 / tool2"


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
    assert result[0].name == "group1 / tool1"
    assert result[0].alias == "t1"

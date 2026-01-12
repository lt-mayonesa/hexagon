import pytest

from hexagon.domain.tool import ActionTool, GroupTool, ToolType
from hexagon.domain.tool_display import ToolDisplayMode
from hexagon.runtime.presentation import tool_display
from hexagon.runtime.singletons import options


@pytest.fixture
def sample_tools():
    """Sample tools with a nested group structure."""
    return [
        ActionTool(name="top-tool-1", alias="t1", action="action1"),
        GroupTool(
            name="group1",
            type=ToolType.group,
            tools=[
                ActionTool(name="nested-tool-1", alias="n1", action="action2"),
                ActionTool(name="nested-tool-2", alias="n2", action="action3"),
            ],
        ),
        ActionTool(name="top-tool-2", alias="t2", action="action4"),
    ]


def test_prepare_tools_for_display_returns_original_tools_when_display_mode_is_tree(
    sample_tools,
):
    """
    Given a list of tools with nested groups.
    When the tool_display_mode is set to 'tree'.
    Then prepare_tools_for_display should return the original tools unchanged.
    """
    # Ensure display mode is tree (default)
    assert options.tool_display_mode == ToolDisplayMode.tree

    result = tool_display.prepare_tools_for_display(sample_tools)

    assert result == sample_tools
    assert result is sample_tools  # Same object reference


def test_prepare_tools_for_display_returns_flattened_list_when_display_mode_is_list(
    sample_tools, monkeypatch
):
    """
    Given a list of tools with nested groups.
    When the tool_display_mode is set to 'list'.
    Then prepare_tools_for_display should return a flattened list view.
    And nested tools should have group context in their long_name.
    And groups should be included for navigation.
    """
    # Set display mode to list
    monkeypatch.setattr(options, "tool_display_mode", ToolDisplayMode.list)

    result = tool_display.prepare_tools_for_display(sample_tools)

    # Should have 5 tools: 2 top-level + group1 + 2 from group1
    assert len(result) == 5

    # Top-level tools should be unchanged
    assert result[0].name == "top-tool-1"
    assert result[0].long_name is None  # No group context for top-level

    # Group should be included
    assert result[1].name == "group1"
    assert result[1].type == ToolType.group

    # Nested tools should have group context
    assert result[2].name == "nested-tool-1"
    assert result[2].long_name == "nested-tool-1 [group1]"
    assert result[2].group_path is not None
    assert len(result[2].group_path) == 1
    assert result[2].group_path[0].name == "group1"

    assert result[3].name == "nested-tool-2"
    assert result[3].long_name == "nested-tool-2 [group1]"

    assert result[4].name == "top-tool-2"
    assert result[4].long_name is None


def test_prepare_tools_for_display_preserves_tool_names_and_aliases(
    sample_tools, monkeypatch
):
    """
    Given a list of tools with nested groups.
    When prepare_tools_for_display transforms to list view.
    Then all tool names and aliases should be preserved exactly.
    And only long_name should be modified for display purposes.
    """
    monkeypatch.setattr(options, "tool_display_mode", ToolDisplayMode.list)

    result = tool_display.prepare_tools_for_display(sample_tools)

    # Check that names and aliases are preserved
    # Result: top-tool-1, group1, nested-tool-1, nested-tool-2, top-tool-2
    assert result[0].name == "top-tool-1"
    assert result[0].alias == "t1"

    assert result[1].name == "group1"
    assert result[1].alias is None

    assert result[2].name == "nested-tool-1"
    assert result[2].alias == "n1"

    assert result[3].name == "nested-tool-2"
    assert result[3].alias == "n2"

    assert result[4].name == "top-tool-2"
    assert result[4].alias == "t2"


def test_prepare_tools_for_display_handles_empty_tool_list():
    """
    Given an empty list of tools.
    When prepare_tools_for_display is called.
    Then it should return an empty list without errors.
    """
    result = tool_display.prepare_tools_for_display([])

    assert result == []

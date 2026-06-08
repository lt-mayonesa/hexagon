"""
Unit tests for hexagon/runtime/execute/list_view.py.

These tests cover:
- flatten_tools  : recursive flattening of the tool tree
- format_breadcrumb : display string generation for all directions / separators
- build_list_choices : InquirerPy-compatible choice list construction
"""

from hexagon.domain.tool import ActionTool, FunctionTool, GroupTool, Separator, ToolType
from hexagon.runtime.execute.list_view import (
    FlatTool,
    build_list_choices,
    flatten_tools,
    format_breadcrumb,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _action(
    name, *, alias=None, long_name=None, description=None, tool_type=ToolType.shell
):
    return ActionTool(
        name=name,
        action=f"echo {name}",
        type=tool_type,
        alias=alias,
        long_name=long_name,
        description=description,
    )


def _group(name, tools, *, alias=None, long_name=None):
    return GroupTool(
        name=name,
        type=ToolType.group,
        tools=tools,
        alias=alias,
        long_name=long_name,
    )


def _function(name):
    return FunctionTool(name=name, type=ToolType.misc, function=lambda: None)


# ---------------------------------------------------------------------------
# flatten_tools
# ---------------------------------------------------------------------------


def test_flatten_tools_returns_empty_for_empty_list():
    """
    Given an empty tools list.
    When flatten_tools is called.
    Then the result is an empty list.
    """
    assert flatten_tools([]) == []


def test_flatten_tools_returns_root_tools_with_empty_path():
    """
    Given two root-level ActionTools.
    When flatten_tools is called.
    Then both are returned with path_tools=[].
    """
    tools = [_action("a"), _action("b")]
    result = flatten_tools(tools)

    assert len(result) == 2
    assert all(ft.path_tools == [] for ft in result)
    assert [ft.tool.name for ft in result] == ["a", "b"]


def test_flatten_tools_explodes_one_group_level():
    """
    Given a group that contains two child tools.
    When flatten_tools is called.
    Then two FlatTool entries are returned with path_tools=[group].
    """
    grp = _group("grp", [_action("child-a"), _action("child-b")])
    result = flatten_tools([grp])

    assert len(result) == 2
    assert all(len(ft.path_tools) == 1 for ft in result)
    assert all(ft.path_tools[0].name == "grp" for ft in result)
    assert [ft.tool.name for ft in result] == ["child-a", "child-b"]


def test_flatten_tools_explodes_nested_groups():
    """
    Given a group that contains a sub-group which contains a tool.
    When flatten_tools is called.
    Then one FlatTool is returned with path_tools=[group, sub-group].
    """
    leaf = _action("leaf")
    sub = _group("sub", [leaf])
    grp = _group("grp", [sub])

    result = flatten_tools([grp])

    assert len(result) == 1
    ft = result[0]
    assert [g.name for g in ft.path_tools] == ["grp", "sub"]
    assert ft.tool.name == "leaf"
    assert ft.path == ["grp", "sub"]


def test_flatten_tools_excludes_group_tools_themselves():
    """
    Given a group with child tools.
    When flatten_tools is called.
    Then no FlatTool entry has a GroupTool as its .tool attribute.
    """
    grp = _group("grp", [_action("child")])
    result = flatten_tools([grp])

    assert all(not isinstance(ft.tool, GroupTool) for ft in result)


def test_flatten_tools_excludes_separators():
    """
    Given a tool list that contains the built-in Separator.
    When flatten_tools is called.
    Then the separator is not present in the result.
    """
    result = flatten_tools([_action("a"), Separator, _action("b")])

    assert len(result) == 2
    assert [ft.tool.name for ft in result] == ["a", "b"]


def test_flatten_tools_excludes_function_tools():
    """
    Given a tool list that contains a FunctionTool.
    When flatten_tools is called.
    Then the FunctionTool is not present in the result.
    """
    result = flatten_tools([_action("a"), _function("fn"), _action("b")])

    assert len(result) == 2
    assert [ft.tool.name for ft in result] == ["a", "b"]


def test_flatten_tools_preserves_order_across_groups():
    """
    Given root tool A, a group containing B and C, and root tool D.
    When flatten_tools is called.
    Then the order is A, B, C, D.
    """
    tools = [
        _action("a"),
        _group("grp", [_action("b"), _action("c")]),
        _action("d"),
    ]
    result = flatten_tools(tools)

    assert [ft.tool.name for ft in result] == ["a", "b", "c", "d"]


def test_flatten_tools_handles_mixed_root_and_nested():
    """
    Given root tools mixed with groups at multiple depths.
    When flatten_tools is called.
    Then each FlatTool has the correct path and tool.
    """
    tools = [
        _action("root-1"),
        _group("g1", [_action("child-1"), _action("child-2")]),
        _action("root-2"),
        _group("g2", [_group("sub", [_action("deep")])]),
    ]
    result = flatten_tools(tools)

    paths = [ft.path for ft in result]
    names = [ft.tool.name for ft in result]

    assert names == ["root-1", "child-1", "child-2", "root-2", "deep"]
    assert paths == [[], ["g1"], ["g1"], [], ["g2", "sub"]]


# ---------------------------------------------------------------------------
# format_breadcrumb
# ---------------------------------------------------------------------------


def _flat(tool, *groups):
    """Build a FlatTool with the given ancestor groups."""
    return FlatTool(
        path_tools=[_group(g, []) for g in groups],
        tool=tool,
    )


def test_format_breadcrumb_rtl_single_group():
    """
    Given a FlatTool with one ancestor group and direction rtl.
    When format_breadcrumb is called.
    Then the result is 'tool | group'.
    """
    ft = _flat(_action("t"), "grp")
    result = format_breadcrumb(ft, "rtl", " | ")

    assert result == "t | grp"


def test_format_breadcrumb_rtl_nested():
    """
    Given a FlatTool nested two levels deep and direction rtl.
    When format_breadcrumb is called.
    Then the result is 'tool | immediate | root'.
    """
    ft = _flat(_action("t"), "root", "sub")
    result = format_breadcrumb(ft, "rtl", " | ")

    assert result == "t | sub | root"


def test_format_breadcrumb_ltr_single_group():
    """
    Given a FlatTool with one ancestor group and direction ltr.
    When format_breadcrumb is called.
    Then the result is 'group | tool'.
    """
    ft = _flat(_action("t"), "grp")
    result = format_breadcrumb(ft, "ltr", " | ")

    assert result == "grp | t"


def test_format_breadcrumb_ltr_nested():
    """
    Given a FlatTool nested two levels deep and direction ltr.
    When format_breadcrumb is called.
    Then the result is 'root | immediate | tool'.
    """
    ft = _flat(_action("t"), "root", "sub")
    result = format_breadcrumb(ft, "ltr", " | ")

    assert result == "root | sub | t"


def test_format_breadcrumb_tool_only():
    """
    Given a FlatTool with ancestor groups and direction tool_only.
    When format_breadcrumb is called.
    Then only the tool name is returned without any separator.
    """
    ft = _flat(_action("t"), "root", "sub")
    result = format_breadcrumb(ft, "tool_only", " | ")

    assert result == "t"


def test_format_breadcrumb_no_groups_rtl():
    """
    Given a root-level FlatTool (no groups) and direction rtl.
    When format_breadcrumb is called.
    Then only the tool name is returned (no trailing separator).
    """
    ft = _flat(_action("t"))
    result = format_breadcrumb(ft, "rtl", " | ")

    assert result == "t"


def test_format_breadcrumb_no_groups_ltr():
    """
    Given a root-level FlatTool (no groups) and direction ltr.
    When format_breadcrumb is called.
    Then only the tool name is returned.
    """
    ft = _flat(_action("t"))
    result = format_breadcrumb(ft, "ltr", " | ")

    assert result == "t"


def test_format_breadcrumb_custom_separator():
    """
    Given separator ' > '.
    When format_breadcrumb is called.
    Then '>' is used instead of '|'.
    """
    ft = _flat(_action("t"), "grp")
    result = format_breadcrumb(ft, "rtl", " > ")

    assert result == "t > grp"


def test_format_breadcrumb_uses_long_name_when_available():
    """
    Given a tool with a long_name and a group with a long_name.
    When format_breadcrumb is called.
    Then long_name values are used for both tool and group in the display.
    """
    tool = _action("t-name", long_name="Tool Long Name")
    ft = FlatTool(
        path_tools=[_group("g-name", [], long_name="Group Long Name")],
        tool=tool,
    )
    result = format_breadcrumb(ft, "rtl", " | ")

    assert result == "Tool Long Name | Group Long Name"


# ---------------------------------------------------------------------------
# build_list_choices
# ---------------------------------------------------------------------------


def test_build_list_choices_value_is_unique_across_groups():
    """
    Given two tools with the same name in different groups.
    When build_list_choices is called.
    Then the resulting choice values are distinct FlatTool objects.
    """
    tools = [
        _group("g1", [_action("tool")]),
        _group("g2", [_action("tool")]),
    ]
    flat = flatten_tools(tools)
    choices = build_list_choices(flat, "rtl", " | ")

    assert len(choices) == 2
    assert choices[0]["value"] is not choices[1]["value"]


def test_build_list_choices_name_contains_description():
    """
    Given a tool with a description.
    When build_list_choices is called.
    Then the description appears in the choice name string.
    """
    tool = _action("t", description="Does something useful")
    flat = flatten_tools([tool])
    choices = build_list_choices(flat, "rtl", " | ")

    assert "Does something useful" in choices[0]["name"]


def test_build_list_choices_name_contains_classifier_icon():
    """
    Given a tool of type web.
    When build_list_choices is called.
    Then the web classifier symbol appears in the choice name string.
    """
    tool = _action("t", tool_type=ToolType.web)
    flat = flatten_tools([tool])
    choices = build_list_choices(flat, "rtl", " | ")

    assert "⦾" in choices[0]["name"]


def test_build_list_choices_value_is_flat_tool_object():
    """
    Given a flat tool list.
    When build_list_choices is called.
    Then each choice value is the FlatTool object itself.
    """
    flat = flatten_tools([_action("t")])
    choices = build_list_choices(flat, "rtl", " | ")

    assert isinstance(choices[0]["value"], FlatTool)
    assert choices[0]["value"] is flat[0]

from typing import List

from hexagon.domain.tool import (
    ActionTool,
    FunctionTool,
    GroupPathItem,
    Separator,
    Tool,
    ToolType,
)


def _should_add_separator_before_group(
    is_top_level: bool, previous_was_group: bool, has_existing_tools: bool
) -> bool:
    return is_top_level and previous_was_group and has_existing_tools


def _format_group_context(prefix: str) -> str:
    return prefix[:-3] if prefix.endswith(" › ") else prefix


def _create_tool_with_group_context(
    tool: Tool, prefix: str, group_path_items: List[GroupPathItem]
) -> Tool:
    tool_dict = tool.model_dump()

    group_context = _format_group_context(prefix)

    if tool.long_name:
        tool_dict["long_name"] = f"{tool.long_name} [{group_context}]"
    else:
        tool_dict["long_name"] = f"{tool.name} [{group_context}]"

    tool_dict["group_path"] = group_path_items if group_path_items else None

    if isinstance(tool, ActionTool):
        return ActionTool(**tool_dict)
    elif isinstance(tool, FunctionTool):
        return FunctionTool(
            **{k: v for k, v in tool_dict.items() if k != "function"},
            function=tool.function,
        )
    else:
        return Tool(**tool_dict)


def _add_group_tools(
    tool, group_prefix: str, current_path: List[GroupPathItem], flattened: List[Tool]
):
    """Add all tools from a group to the flattened list with context."""
    for child_tool in tool.tools:
        if child_tool.type == ToolType.separator:
            continue
        elif child_tool.type == ToolType.group:
            nested_tools = list_view(
                [child_tool],
                group_prefix,
                is_top_level=False,
                group_path_items=current_path,
            )
            flattened.extend(nested_tools)
        else:
            flattened.append(
                _create_tool_with_group_context(child_tool, group_prefix, current_path)
            )


def list_view(
    tools: List[Tool],
    prefix: str = "",
    is_top_level: bool = True,
    group_path_items: List[GroupPathItem] = None,
) -> List[Tool]:
    """
    Transform tools for flat list display while preserving navigation structure.

    Unlike tree view, this shows all tools (including from nested groups) in one list,
    but keeps the group structure intact for navigation. This means:
    - Groups are still present and navigable (e.g., 'cli group1' works)
    - Tools show their group context in brackets: 'Tool Three [group1]'
    - CLI commands work the same in both tree and list views

    The key difference from tree view is purely visual - all tools are shown
    in one flat list instead of nested menus.
    """
    if group_path_items is None:
        group_path_items = []

    flattened = []
    previous_was_group = False

    for tool in tools:
        if tool.type == ToolType.separator:
            if not prefix:
                flattened.append(tool)
            continue

        if tool.type == ToolType.group:
            if _should_add_separator_before_group(
                is_top_level, previous_was_group, bool(flattened)
            ):
                flattened.append(Separator)

            # Add the group tool itself (for navigation)
            if prefix:
                flattened.append(
                    _create_tool_with_group_context(tool, prefix, group_path_items)
                )
            else:
                flattened.append(tool)

            group_prefix = f"{prefix}{tool.long_name or tool.name} › "
            current_path = group_path_items + [
                GroupPathItem(name=tool.name, alias=tool.alias)
            ]

            _add_group_tools(tool, group_prefix, current_path, flattened)
            previous_was_group = True
        else:
            if prefix:
                flattened.append(
                    _create_tool_with_group_context(tool, prefix, group_path_items)
                )
            else:
                flattened.append(tool)

            previous_was_group = False

    return flattened

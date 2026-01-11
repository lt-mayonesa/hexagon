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


def list_view(
    tools: List[Tool],
    prefix: str = "",
    is_top_level: bool = True,
    group_path_items: List[GroupPathItem] = None,
) -> List[Tool]:
    """
    Transform a tree of tools into a flat list for display.

    The display long_name shows group context in brackets: 'Tool Three [group1]'
    but the actual tool name and alias remain unchanged to preserve CLI commands.

    This ensures that 'cli group1 tool3' works the same in both tree and list views.

    - Tool names and aliases are preserved (no changes to command structure)
    - long_name is modified to show group context for display
    - group_path metadata stores structured group ancestry for tracing
    - Separators inside nested groups are filtered out
    - Visual separators are added between top-level groups
    - Empty groups contribute nothing to the output
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

            group_prefix = f"{prefix}{tool.name} › " if tool.name else prefix
            current_path = group_path_items + [
                GroupPathItem(name=tool.name, alias=tool.alias)
            ]
            group_tools = list_view(
                tool.tools,
                group_prefix,
                is_top_level=False,
                group_path_items=current_path,
            )
            flattened.extend(group_tools)

            if group_tools:
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

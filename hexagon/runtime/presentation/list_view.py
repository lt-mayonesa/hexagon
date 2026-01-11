from typing import List

from hexagon.domain.tool import (
    ActionTool,
    FunctionTool,
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


def _create_tool_with_group_context(tool: Tool, prefix: str) -> Tool:
    tool_dict = tool.model_dump()
    original_name = tool.name

    group_context = _format_group_context(prefix)
    tool_dict["name"] = f"{tool.name} [{group_context}]"

    if tool.long_name:
        tool_dict["long_name"] = f"{tool.long_name} [{group_context}]"

    if not tool.alias:
        tool_dict["alias"] = original_name

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
    tools: List[Tool], prefix: str = "", is_top_level: bool = True
) -> List[Tool]:
    """
    Transform a tree of tools into a flat list for display.

    Tools from groups are shown with their name first followed by group context
    in brackets: 'migrate [database › admin]'

    - Original tool names are preserved as aliases for CLI selection
    - Separators inside nested groups are filtered out
    - Visual separators are added between top-level groups
    - Empty groups contribute nothing to the output
    """
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
            group_tools = list_view(tool.tools, group_prefix, is_top_level=False)
            flattened.extend(group_tools)

            if group_tools:
                previous_was_group = True
        else:
            if prefix:
                flattened.append(_create_tool_with_group_context(tool, prefix))
            else:
                flattened.append(tool)

            previous_was_group = False

    return flattened

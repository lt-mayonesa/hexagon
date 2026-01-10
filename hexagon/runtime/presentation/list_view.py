from typing import List

from hexagon.domain.tool import (
    ActionTool,
    FunctionTool,
    Separator,
    Tool,
    ToolType,
)


def _create_flattened_tool(tool: Tool, prefix: str) -> Tool:
    """
    Helper to create a flattened tool with group context in brackets.
    """
    tool_dict = tool.model_dump()
    original_name = tool.name

    # Format: "tool_name [group1 › group2]"
    group_context = prefix[:-3] if prefix.endswith(" › ") else prefix
    tool_dict["name"] = f"{tool.name} [{group_context}]"

    # Keep long_name and add group context
    if tool.long_name:
        tool_dict["long_name"] = f"{tool.long_name} [{group_context}]"

    # Preserve alias if it exists, otherwise use original name for CLI selection
    if not tool.alias:
        tool_dict["alias"] = original_name

    # Create new tool instance with modified name
    if isinstance(tool, ActionTool):
        return ActionTool(**tool_dict)
    elif isinstance(tool, FunctionTool):
        # Preserve the original function reference (can't serialize callables)
        return FunctionTool(
            **{k: v for k, v in tool_dict.items() if k != "function"},
            function=tool.function,
        )
    else:
        return Tool(**tool_dict)


def flatten_tools(
    tools: List[Tool], prefix: str = "", is_top_level: bool = True
) -> List[Tool]:
    """
    Recursively flatten a tree of tools into a single list.
    Tool names are shown first with group context in brackets: 'tool3 [group1]'.
    The original tool name is preserved in the alias if no alias exists,
    allowing selection by original name from CLI args.
    Separators are filtered out from nested groups and added between top-level groups.
    """
    flattened = []
    previous_was_group = False

    for tool in tools:
        # Skip separators in nested groups
        if tool.type == ToolType.separator:
            if not prefix:  # Only keep separators at top level
                flattened.append(tool)
            continue

        if tool.type == ToolType.group:
            # Add separator before group at top level (except for first group)
            if is_top_level and previous_was_group and flattened:
                flattened.append(Separator)

            # Add group prefix to all nested tools
            group_prefix = f"{prefix}{tool.name} › " if tool.name else prefix
            group_tools = flatten_tools(tool.tools, group_prefix, is_top_level=False)
            flattened.extend(group_tools)

            # Track that we've seen a group (only if it had tools)
            if group_tools:
                previous_was_group = True
        else:
            # Clone the tool with modified name if there's a prefix
            if prefix:
                flattened.append(_create_flattened_tool(tool, prefix))
            else:
                flattened.append(tool)

            previous_was_group = False

    return flattened

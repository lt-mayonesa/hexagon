from typing import List

from hexagon.domain.tool import Tool
from hexagon.domain.tool_display import ToolDisplayMode
from hexagon.runtime.presentation.list_view import list_view
from hexagon.runtime.singletons import options


def prepare_tools_for_display(tools: List[Tool]) -> List[Tool]:
    """
    Prepare tools for display based on the configured display mode.

    Returns either the original tree structure or a flattened list view
    depending on the tool_display_mode option.
    """
    if options.tool_display_mode == ToolDisplayMode.list:
        return list_view(tools)

    return tools

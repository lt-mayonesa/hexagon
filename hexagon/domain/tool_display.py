from enum import Enum


class ToolDisplayMode(str, Enum):
    """
    Tool display mode for the CLI menu.

    - tree: Default tree view with groups (traditional hierarchical display)
    - list: Single list view with prefixed tool names (all tools in one list)
    """

    tree = "tree"
    list = "list"

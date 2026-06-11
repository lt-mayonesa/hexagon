from dataclasses import dataclass
from typing import Callable, List, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import FunctionTool, GroupTool, Tool, ToolType


@dataclass
class FlatTool:
    """
    A leaf tool together with its full ancestor path through the group tree.

    ``path_tools`` holds the sequence of ``GroupTool`` objects from the root
    down to (but not including) the leaf tool itself.  Root-level tools have
    an empty ``path_tools``.
    """

    path_tools: List[GroupTool]
    tool: Tool

    @property
    def path(self) -> List[str]:
        return [g.name for g in self.path_tools]


def flatten_tools(
    tools: List[Tool],
    _ancestors: Optional[List[GroupTool]] = None,
) -> List[FlatTool]:
    """
    Recursively walk *tools* and return every leaf tool with its ancestor path.

    Excluded from the flat list:
    - ``GroupTool`` items themselves (their children are included instead).
    - ``FunctionTool`` items (internal tools such as separators and go-back).
    """
    if _ancestors is None:
        _ancestors = []
    result = []
    for tool in tools:
        if isinstance(tool, FunctionTool) or tool.type == ToolType.separator:
            continue
        if isinstance(tool, GroupTool):
            result.extend(flatten_tools(tool.tools, _ancestors + [tool]))
        else:
            result.append(FlatTool(path_tools=list(_ancestors), tool=tool))
    return result


def format_breadcrumb(flat_tool: FlatTool, direction: str, separator: str) -> str:
    """
    Return the display string for *flat_tool* according to *direction*.

    ``rtl``       – deepest-first:   ``tool | immediate-group | root-group``
    ``ltr``       – root-first:      ``root-group | immediate-group | tool``
    ``tool_only`` – no breadcrumb:   ``tool``
    """
    tool_display = flat_tool.tool.long_name or flat_tool.tool.name
    group_names = [g.long_name or g.name for g in flat_tool.path_tools]

    if direction == "tool_only" or not group_names:
        return tool_display

    if direction == "ltr":
        parts = group_names + [tool_display]
    else:  # rtl (default)
        parts = [tool_display] + list(reversed(group_names))

    return separator.join(parts)


def _tool_classifier(tool: Tool) -> str:
    if tool.icon:
        return f"{tool.icon:2}"
    symbols = {"web": "⦾", "shell": "ƒ", "misc": " ", "hexagon": "⬡", "group": "≡"}
    r = symbols.get(tool.type, "")
    return f"{r:2}" if r else ""


def build_list_choices(
    flat_tools: List[FlatTool],
    direction: str,
    separator: str,
) -> List[dict]:
    """
    Build InquirerPy-compatible choice dicts for the flat tool list.

    Each ``value`` is the ``FlatTool`` object itself so the caller gets it back
    directly from the prompt without a second lookup.
    """
    choices = []
    for ft in flat_tools:
        breadcrumb = format_breadcrumb(ft, direction, separator)
        gap = 60 if ft.tool.description else 0
        name = f"{_tool_classifier(ft.tool) + breadcrumb: <{gap}}{ft.tool.description or ''}"
        choices.append({"value": ft, "name": name})
    return choices


def select_and_execute_list_view(
    tools: List[Tool],
    envs: List[Env],
    cli_args,
    execute_leaf_fn: Callable,
) -> List[str]:
    """
    Present a single flat fuzzy-searchable prompt that contains *all* leaf
    tools across every group level, then execute the selected tool.

    Tracing mirrors tree-mode: each group in the ancestor path is recorded
    under ``tool_<depth>`` so that the resulting trace is replayable with
    the same positional-arg tree-style resolution.

    ``execute_leaf_fn`` is injected by the caller (``_execute_leaf_tool`` from
    ``tool.py``) to avoid a circular import.
    """
    from hexagon.runtime.singletons import options
    from hexagon.runtime.wax import _select_and_register_event
    from hexagon.support.tracer import tracer

    flat_tools = flatten_tools(tools)
    choices = build_list_choices(
        flat_tools,
        options.view_mode_direction,
        options.view_mode_separator,
    )

    selected: FlatTool = cli_args.__prompt__.fuzzy(
        choices=choices,
        message=_("action.support.wax.select_tool"),
    )

    # Fire selection hooks and record trace for every group in the path so that
    # the resulting trace is identical to what tree-mode would have produced.
    for i, group in enumerate(selected.path_tools):
        _select_and_register_event(group.name, [group], target="tool", prompted=True)
        if group.traced:
            tracer().tracing(f"tool_{i}", group.name, value_alias=group.alias)

    leaf_ref = len(selected.path_tools)
    leaf = selected.tool

    _select_and_register_event(leaf.name, [leaf], target="tool", prompted=True)
    if leaf.traced:
        tracer().tracing(f"tool_{leaf_ref}", leaf.name, value_alias=leaf.alias)

    return execute_leaf_fn(leaf, envs, cli_args, group_ref=leaf_ref)

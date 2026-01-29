from typing import Union, List, Tuple

from hexagon.domain.env import Env
from hexagon.domain.hooks.wax import Selection, SelectionType
from hexagon.domain.tool import Tool, Separator, GroupTool
from hexagon.support.hooks import HexagonHooks
from hexagon.support.input.prompt import prompt


def __classifier(value: Union[Tool, Env]):
    if value.icon:
        return f"{value.icon:2}"

    symbols = {
        "web": "⦾",
        "shell": "ƒ",
        "misc": " ",
        "hexagon": "⬡",
        "group": "≡",
    }
    r = symbols.get(value.type, "")
    return f"{r:2}" if r else ""


def __choices_with_long_name(
    choices: List[Union[Tool, Env]], classifier=lambda x: "", group_context=None
):
    def build_display(v: Union[Tool, Env]):
        if Separator.name in v.name:
            return "--------------------------------------------------------------------------------"
        else:
            # Add group context if available
            name_with_context = v.long_name or v.name
            if group_context and hasattr(v, "name") and v.name in group_context:
                context = group_context[v.name]
                name_with_context = f"{name_with_context}  [{context}]"

            gap = 60 if v.description else 0
            return f"{classifier(v) + name_with_context: <{gap}}{v.description or ''}"

    return [{"value": each.name, "name": build_display(each)} for each in choices]


def search_by_name_or_alias(data: List[Union[Tool, Env]], arg: str):
    if arg:
        for k in data:
            if k.name == arg or k.alias == arg:
                return k.name

    return None


def flatten_tools_for_list_view(
    tools: List[Tool], parent_path: List[str] = None
) -> Tuple[List[Tool], dict]:
    """
    Flatten a list of tools including nested group tools.

    Returns a tuple of (flattened_tools, group_context_map) where:
    - flattened_tools: All tools including groups and their nested tools
    - group_context_map: Dict mapping tool names to their group path string
    """
    if parent_path is None:
        parent_path = []

    flattened = []
    group_context = {}

    for tool in tools:
        # Always add the tool itself (including groups)
        flattened.append(tool)

        # If it's a group, also add its nested tools
        if isinstance(tool, GroupTool) and isinstance(tool.tools, list):
            current_path = parent_path + [tool.long_name or tool.name]
            nested_tools, nested_context = flatten_tools_for_list_view(
                tool.tools, current_path
            )

            # Add all nested tools and groups
            flattened.extend(nested_tools)

            # Merge context maps
            group_context.update(nested_context)

            # Add context for direct children only
            for nested_tool in tool.tools:
                path_str = " → ".join(current_path)
                group_context[nested_tool.name] = path_str

    return flattened, group_context


def select_env(available_envs: List[Env], tool_envs: dict = None, selected: str = None):
    if not tool_envs:
        return None, None

    if "*" in tool_envs:
        return None, tool_envs["*"]

    (env, prompted) = (
        (selected, False)
        if selected
        else (
            prompt.fuzzy(
                message=_("action.support.wax.select_environment"),
                choices=__choices_with_long_name(
                    [e for e in available_envs if e.name in tool_envs.keys()]
                ),
                validate=lambda x: x and Separator.name not in x,
                invalid_message=_("error.support.wax.invalid_environment"),
            ),
            True,
        )
    )

    return (
        _select_and_register_event(env, available_envs, prompted, target="env"),
        tool_envs[env],
    )


def select_tool(tools: List[Tool], selected: str = None, use_list_view: bool = False):
    if selected:
        return _select_and_register_event(selected, tools, target="tool")

    # In list view mode, flatten the tools
    display_tools = tools
    group_context = None
    if use_list_view:
        display_tools, group_context = flatten_tools_for_list_view(tools)

    name = prompt.fuzzy(
        message=_("action.support.wax.select_tool"),
        choices=__choices_with_long_name(
            display_tools, classifier=__classifier, group_context=group_context
        ),
        validate=lambda x: x and Separator.name not in x,
        invalid_message=_("error.support.wax.invalid_tool"),
    )

    # Find the selected tool in the original tools list (including nested groups)
    return _select_and_register_event(
        name, display_tools if use_list_view else tools, target="tool", prompt=True
    )


def _select_and_register_event(
    name: str, options: List[Union[Tool, Env]], prompt=False, **kwargs
):
    selected = next((e for e in options if e.name == name), None)
    if selected:
        selection = Selection(
            selected, SelectionType.prompt if prompt else SelectionType.args, **kwargs
        )
        if isinstance(selected, Tool):
            HexagonHooks.tool_selected.run(selection)
        elif isinstance(selected, Env):
            HexagonHooks.env_selected.run(selection)
    return selected

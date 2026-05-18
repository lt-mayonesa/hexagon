from typing import Union, List

from hexagon.domain.env import Env
from hexagon.domain.hooks.wax import Selection, SelectionType
from hexagon.domain.tool import Tool
from hexagon.support.hooks import HexagonHooks


def search_by_name_or_alias(data: List[Union[Tool, Env]], arg: str):
    if arg:
        for k in data:
            if k.name == arg or k.alias == arg:
                return k.name

    return None


def _select_and_register_event(
    name: str,
    candidates: List[Union[Tool, Env]],
    *,
    target: str,
    prompted: bool = False,
):
    selected = next((e for e in candidates if e.name == name), None)
    if selected:
        selection = Selection(
            selected,
            SelectionType.prompt if prompted else SelectionType.args,
            target=target,
        )
        if isinstance(selected, Tool):
            HexagonHooks.tool_selected.run(selection)
        elif isinstance(selected, Env):
            HexagonHooks.env_selected.run(selection)
    return selected

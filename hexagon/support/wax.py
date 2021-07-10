from typing import Dict, Union

from InquirerPy import inquirer

from hexagon.domain.env import Env
from hexagon.domain.tool import Tool


def __classifier(value: Tool):
    symbols = {"web": "⦾", "shell": "ƒ", "misc": " ", "hexagon": "⬡"}
    r = symbols.get(value.type, "")
    return f"{r:2}" if r else ""


def __choices_with_long_name(dic: Dict[str, Union[Tool, Env]], classifier=lambda x: ""):
    def build_display(v: Union[Tool, Env], k: str):
        if "__separator" in k:
            return "--------------------------------------------------------------------------------"
        else:
            gap = 60 if v.description else 0
            return f"{classifier(v) + (v.long_name or k): <{gap}}{v.description or ''}"

    return [{"value": k, "name": build_display(v, k)} for k, v in dic.items()]


def search_by_key_or_alias(dic: Dict[str, Union[Tool, Env]], arg: str):
    if arg:
        for k, v in dic.items():
            if k == arg or v.alias == arg:
                return k

    return None


def select_env(
    available_envs: Dict[str, Env], tool_envs: dict = None, selected: str = None
):
    if not tool_envs:
        return None, None

    if "*" in tool_envs:
        return None, tool_envs["*"]

    if selected:
        return selected, tool_envs[selected]

    qs = {k: available_envs[k] for k in tool_envs.keys()}

    env = inquirer.fuzzy(
        message="On which environment?",
        choices=__choices_with_long_name(qs),
        validate=lambda x: x and "__separator" not in x,
        invalid_message="Please select a valid environment",
    ).execute()

    return env, tool_envs[env]


def select_tool(tools_dict: Dict[str, Tool], selected: str = None):
    if selected:
        return selected, tools_dict[selected]

    name = inquirer.fuzzy(
        message="Hi, which tool would you like to use today?",
        choices=__choices_with_long_name(tools_dict, classifier=__classifier),
        validate=lambda x: x and "__separator" not in x,
        invalid_message="Please select a valid tool",
    ).execute()

    return name, tools_dict[name]

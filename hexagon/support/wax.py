from typing import Union, List

from InquirerPy import inquirer

from hexagon.domain.env import Env
from hexagon.domain.tool import Tool


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


def __choices_with_long_name(choices: List[Union[Tool, Env]], classifier=lambda x: ""):
    def build_display(v: Union[Tool, Env]):
        if "__separator" in v.name:
            return "--------------------------------------------------------------------------------"
        else:
            gap = 60 if v.description else 0
            return f"{classifier(v) + (v.long_name or v.name): <{gap}}{v.description or ''}"

    return [{"value": each.name, "name": build_display(each)} for each in choices]


def search_by_name_or_alias(data: List[Union[Tool, Env]], arg: str):
    if arg:
        for k in data:
            if k.name == arg or k.alias == arg:
                return k.name

    return None


def select_env(available_envs: List[Env], tool_envs: dict = None, selected: str = None):
    if not tool_envs:
        return None, None

    if "*" in tool_envs:
        return None, tool_envs["*"]

    env = (
        selected
        or inquirer.fuzzy(
            message="On which environment?",
            choices=__choices_with_long_name(
                [e for e in available_envs if e.name in tool_envs.keys()]
            ),
            validate=lambda x: x and "__separator" not in x,
            invalid_message="Please select a valid environment",
        ).execute()
    )

    return next((e for e in available_envs if e.name == env), None), tool_envs[env]


def select_tool(tools: List[Tool], selected: str = None):
    if selected:
        return next(t for t in tools if t.name == selected)

    name = inquirer.fuzzy(
        message="Hi, which tool would you like to use today?",
        choices=__choices_with_long_name(tools, classifier=__classifier),
        validate=lambda x: x and "__separator" not in x,
        invalid_message="Please select a valid tool",
    ).execute()

    return next(t for t in tools if t.name == name)

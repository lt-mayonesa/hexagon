from InquirerPy import inquirer


def __classifier(value):
    symbols = {"web": "⦾", "shell": "ƒ", "misc": " ", "hexagon": "⬡"}
    r = symbols.get(value.get("type", "misc"), "")
    return f"{r:2}" if r else ""


def __choices_with_long_name(dic, classifier=lambda x: ""):
    def build_display(v, k):
        if "__separator" in k:
            return "--------------------------------------------------------------------------------"
        else:
            gap = 60 if "description" in v else 0
            return f"{classifier(v) + v.get('long_name', k): <{gap}}{v.get('description', '')}"

    return [{"value": k, "name": build_display(v, k)} for k, v in dic.items()]


def search_by_key_or_alias(dic, arg):
    if arg:
        for k, v in dic.items():
            if k == arg or v.get("alias") == arg:
                return k

    return None


def select_env(available_envs: dict, tool_envs: dict = None, selected=None):
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


def select_tool(tools_dict: dict, selected=None):
    if selected:
        return selected, tools_dict[selected]

    name = inquirer.fuzzy(
        message="Hi, which tool would you like to use today?",
        choices=__choices_with_long_name(tools_dict, classifier=__classifier),
        validate=lambda x: x and "__separator" not in x,
        invalid_message="Please select a valid tool",
    ).execute()

    return name, tools_dict[name]

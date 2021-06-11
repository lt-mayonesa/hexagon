from InquirerPy import prompt


def tool_questions(choices):
    return [
        {
            'type': 'fuzzy',
            'name': 'tool',
            'message': 'Hi, which tool would you like to use today?',
            'choices': choices,
            'validate': lambda x: x,
            'invalid_message': 'Please select a valid tool'
        }
    ]


def env_questions(choices):
    return [
        {
            'type': 'fuzzy',
            'name': 'env',
            'message': 'On which environment?',
            'choices': choices,
            'validate': lambda x: x,
            'invalid_message': 'Please select a valid environment'
        }
    ]


def key_and_alias(dic):
    return [[k, v['alias']] for k, v in dic.items()]


def choices_with_long_name(dic):
    return [{
        'value': k,
        'name': f"{v['long_name']: <60}{v['description'] if 'description' in v else ''}" if 'long_name' in v else k,
        'type': v['type'] if 'type' in v else 'misc'
        # FIXME: this is a quick solution for sorting when tool.type is missing
    } for k, v in dic.items()]


def key_or_alias(dic, arg):
    if arg:
        for k, v in dic.items():
            if k == arg or v['alias'] == arg:
                return k

    return None


def select_env(available_envs: dict, tool_envs: dict, selected):
    if selected:
        return selected, tool_envs[selected]

    if not tool_envs:
        return None, None

    if '*' in tool_envs:
        return None, tool_envs['*']

    qs = {k: available_envs[k] for k in tool_envs.keys()}
    env = prompt(env_questions(choices_with_long_name(qs)))['env']
    return env, tool_envs[env]


def select_tool(tools_dict: dict, selected):
    choices = choices_with_long_name(tools_dict)
    choices.sort(key=lambda x: x["type"], reverse=True)
    name = selected or prompt(tool_questions(choices))['tool']
    return name, tools_dict[name]

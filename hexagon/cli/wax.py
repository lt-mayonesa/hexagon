from InquirerPy import prompt


def tool_questions(choices):
    return [
        {
            'type': 'fuzzy',
            'name': 'tool',
            'message': 'Hola, ¿qué herramienta querés usar hoy?',
            'choices': choices,
            'validate': lambda x: x,
            'invalid_message': 'seleccionar una herramienta valida'
        }
    ]


def env_questions(choices):
    return [
        {
            'type': 'fuzzy',
            'name': 'env',
            'message': '¿Para qué ambiente?',
            'choices': choices,
            'validate': lambda x: x,
            'invalid_message': 'seleccionar un ambiente valido'
        }
    ]


def key_and_alias(dic):
    return [[k, v['alias']] for k, v in dic.items()]


def choices_with_long_name(dic):
    return [{
        'value': k,
        'name': f"{v['long_name']: <60}{v['description'] if 'description' in v else ''}" if 'long_name' in v else k
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
    name = selected or prompt(tool_questions(choices_with_long_name(tools_dict)))['tool']
    return name, tools_dict[name]

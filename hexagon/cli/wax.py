from InquirerPy import inquirer


def __choices_with_long_name(dic):
    def classifier(value):
        symbols = {
            'web': u'⦾',
            'shell': u'ƒ',
            'misc': ' ',
            'hexagon': u'⬡'
        }
        r = symbols.get(value.get('type', 'misc'), '')
        return f'{r:2}' if r else ''

    def build_display(v, k):
        if '__separator' in k:
            return '--------------------------------------------------------------------------------'
        else:
            return f"{classifier(v) + v['long_name']: <60}{v.get('description', '')}" if 'long_name' in v else k

    return [{
        'value': k,
        'name': build_display(v, k)
    } for k, v in dic.items()]


def search_by_key_or_alias(dic, arg):
    if arg:
        for k, v in dic.items():
            if k == arg or v.get('alias') == arg:
                return k

    return None


def select_env(available_envs: dict, tool_envs: dict = None, selected=None):
    if not tool_envs:
        return None, None

    if '*' in tool_envs:
        return None, tool_envs['*']

    if selected:
        return selected, tool_envs[selected]

    qs = {k: available_envs[k] for k in tool_envs.keys()}

    env = inquirer.fuzzy(
        message='On which environment?',
        choices=__choices_with_long_name(qs),
        validate=lambda x: x and '__separator' not in x,
        invalid_message='Please select a valid environment'
    ).execute()

    return env, tool_envs[env]


def select_tool(tools_dict: dict, selected=None):
    if selected:
        return selected, tools_dict[selected]

    name = inquirer.fuzzy(
        message='Hi, which tool would you like to use today?',
        choices=__choices_with_long_name(tools_dict),
        validate=lambda x: x and '__separator' not in x,
        invalid_message='Please select a valid tool'
    ).execute()

    return name, tools_dict[name]

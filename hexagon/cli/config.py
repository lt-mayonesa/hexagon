import os

from ruamel.yaml import YAML


def init_config(path=None):
    __defaults = {
        'cli': {'name': 'Hexagon'},
        'tools': {
            'save-alias': {
                'long_name': 'Save Last Command as Linux Alias',
                'type': 'hexagon',
                'action': 'hexagon.tools.internal.save_new_alias'
            },
            'create-tool': {
                'long_name': 'Create A New Tool',
                'type': 'hexagon',
                'action': 'hexagon.tools.internal.create_new_tool'
            }
        },
        'envs': {}
    }
    try:
        src = path if path else os.getenv('HEXAGON_CONFIG_FILE', 'app.yaml')
        with open(src, 'r') as f:
            __config = YAML().load(f)
    except FileNotFoundError:
        return __initial_setup_config()

    return (
        {
            **__defaults["cli"],
            **__config["cli"]
        },
        {**__add_hexagon_tools(__config, __defaults)},
        {
            **__defaults["envs"],
            **__config['envs']
        }
    )


def __initial_setup_config():
    return (
        {'name': 'Hexagon'},
        {
            'install': {
                'long_name': 'Install CLI',
                'description': 'Install a custom project CLI from a YAML file.',
                'type': 'hexagon',
                'action': 'install_cli'
            }
        },
        {}
    )


def __add_hexagon_tools(__config, __defaults):
    tools = __config['tools']
    tools.update(__defaults['tools'])
    return tools

import os

import yaml


def init_config(path=None):
    __defaults = {
        'cli': {'name': 'Hexagon'},
        'tools': {
            'save-alias': {
                'long_name': 'Save Last Command as Linux Alias',
                'type': 'hexagon',
                'action': 'save_new_alias'
            },
            'install': {
                'long_name': 'Install CLI',
                'description': 'Install a custom project CLI from a YAML file.',
                'type': 'hexagon',
                'action': 'install_hexagon'
            }
        },
        'envs': {}
    }
    try:
        src = path if path else os.getenv('HEXAGON_CONFIG_FILE', 'app.yaml')
        with open(src, 'r') as f:
            __config = yaml.load(f, Loader=yaml.CLoader)
    except FileNotFoundError:
        __config = {'cli': {}, 'tools': {}, 'envs': {}}

    return (
        {
            **__defaults["cli"],
            **__config["cli"]
        },
        {
            **__defaults['tools'],
            **__config['tools']
        },
        {
            **__defaults["envs"],
            **__config['envs']
        }
    )

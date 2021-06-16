import importlib
import os
import sys

from rich import print


def register_external_tools(src: dict):
    if 'custom_tools_dir' in src:
        config_dir = os.environ['HEXAGON_CONFIG_FILE'].replace('app.yaml', '').replace('app.yml', '')
        sys.path.append(config_dir + src['custom_tools_dir'])


def execute_action(action_id: str, args):
    tool_action_module = _load_action_module(action_id) or \
                         _load_action_module(f'hexagon.tools.external.{action_id}')

    if not tool_action_module:
        print(f'[red]Hexagon did not find the action [bold]{action_id}')
        print(f'[red][dim]We checked:')
        print(f'[red][dim]     - Your CLI\'s custom_tools_dir')
        print(f'[red][dim]     - Hexagon repository of externals tools (hexagon.tools.external)')
        sys.exit(1)

    try:
        tool_action_module.main(args)
    except AttributeError:
        print(f'[red]Tool {action_id} does not have the required `main(args...)` function.')
        sys.exit(1)


def _load_action_module(action_id):
    try:
        return __load_module(action_id)
    except ModuleNotFoundError:
        return None


def __load_module(module):
    if module in sys.modules:
        return sys.modules[module]

    return importlib.import_module(module)

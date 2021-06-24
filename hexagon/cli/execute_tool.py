import importlib
import subprocess
import sys

from rich import print

from hexagon.cli.config import cli, configuration


def register_external_tools():
    if 'custom_tools_dir' in cli:
        sys.path.append(configuration.project_path + cli['custom_tools_dir'])


def execute_action(action_id: str, args):
    ext = action_id.split('.')[-1]
    action = {
        'js': _execute_js,
        'sh': _execute_sh
    }.get(ext)

    if action:
        action(action_id, args)
    elif _is_internal_action(action_id) or __has_no_extension(action_id):
        _execute_python_module(action_id, args)
    else:
        print(f'[red]Executor for extension [bold]{ext}[/bold] not known [dim](supported: .js, .sh).')
        sys.exit(1)


def _is_internal_action(action_id):
    return 'hexagon.tools.internal.' in action_id


def __has_no_extension(action_id):
    return action_id.count('.') == 0


def _execute_python_module(action_id, args):
    tool_action_module = _load_action_module(action_id) or _load_action_module(f'hexagon.tools.external.{action_id}')

    if not tool_action_module:
        print(f'[red]Hexagon did not find the action [bold]{action_id}')
        print('[red][dim]We checked:')
        print('[red][dim]     - Your CLI\'s custom_tools_dir')
        print('[red][dim]     - Hexagon repository of externals tools (hexagon.tools.external)')
        sys.exit(1)
    try:
        tool_action_module.main(args)
    except AttributeError as e:
        print(f'[red]Execution of tool [bold]{action_id}[/bold] thru: {e}')
        print('[red]Does it have the required `main(args...)` method?')
        sys.exit(1)


def _execute_js(action_id, args):
    a = __sanitize_args_for_command(args)
    subprocess.call(['node', action_id] + a)


def _execute_sh(action_id, args):
    a = __sanitize_args_for_command(args)
    subprocess.call(['bash', action_id] + a)


def __sanitize_args_for_command(args):
    if isinstance(args, (int, float, complex, str)):
        a = [args]
    else:
        try:
            a = [f'{k}={v}' for k, v in args.items()]
        except AttributeError:
            a = list(args)
    return a


def _load_action_module(action_id):
    try:
        return __load_module(action_id)
    except ModuleNotFoundError:
        return None


def __load_module(module):
    if module in sys.modules:
        return sys.modules[module]

    return importlib.import_module(module)

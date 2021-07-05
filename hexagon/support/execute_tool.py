import importlib
import subprocess
import sys
import os
from typing import List, Union, Dict

from hexagon.cli import configuration
from hexagon.support.printer import log

_command_by_file_extension = {"js": "node", "sh": "bash"}


def execute_action(action, env_args, env, args):
    action_to_execute: str = action["action"]
    ext = action_to_execute.split(".")[-1]
    script_action_command = (
        _command_by_file_extension[ext] if ext in _command_by_file_extension else None
    )

    if script_action_command:
        _execute_script(
            script_action_command, action_to_execute, env_args or [], env, args
        )
    elif _is_internal_action(action_to_execute) or __has_no_extension(
        action_to_execute
    ):
        _execute_python_module(action_to_execute, action, env, env_args, args)
    else:
        log.error(
            f"Executor for extension [bold]{ext}[/bold] not known [dim](supported: .js, .sh)."
        )
        sys.exit(1)


def _is_internal_action(action_id):
    return "hexagon.tools.internal." in action_id


def __has_no_extension(action_id):
    return action_id.count(".") == 0


def _execute_python_module(action_id, action, env, env_args, args):
    tool_action_module = _load_action_module(action_id) or _load_action_module(
        f"hexagon.tools.external.{action_id}"
    )

    if not tool_action_module:
        log.error(f"Hexagon did not find the action [bold]{action_id}")
        log.error("[dim]We checked:")
        log.error(
            f"[dim]     - Your CLI's custom_tools_dir: [bold]{configuration.custom_tools_path}"
        )
        log.error(
            "[dim]     - Hexagon repository of externals tools (hexagon.tools.external)"
        )
        sys.exit(1)
    try:
        tool_action_module.main(action, env, env_args, args)
    except AttributeError as e:
        log.error(f"Execution of tool [bold]{action_id}[/bold] thru: {e}")
        log.error("Does it have the required `main(args...)` method?")
        sys.exit(1)


def _execute_script(command: str, script: str, env_args, env, args):
    # Script should be relative to the project path
    script_path = os.path.join(configuration.project_path, script)
    if env and "alias" in env:
        del env["alias"]
    args = __sanitize_args_for_command(env_args, env, *args)
    subprocess.call([command, script_path] + args)


def __sanitize_args_for_command(*args: Union[List[any], Dict]):
    positional = []
    named = []
    for arg in args:
        if isinstance(arg, (int, float, complex, str)):
            positional.append(str(arg))
        elif isinstance(arg, list):
            for a in arg:
                positional.append(str(a))
        elif not arg:
            continue
        else:
            try:
                named += [f"{k}={v}" for k, v in arg.items() if v]
            except AttributeError:
                # Unknown arg type, try to append it directly
                positional.append(str(arg))
    return named + positional


def _load_action_module(action_id):
    try:
        return __load_module(action_id)
    except ModuleNotFoundError:
        return None


def __load_module(module):
    if module in sys.modules:
        return sys.modules[module]

    return importlib.import_module(module)

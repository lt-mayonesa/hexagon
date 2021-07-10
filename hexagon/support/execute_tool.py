import importlib
import subprocess
import sys
import os
from typing import List, Union, Dict

from hexagon.domain.tool import Tool
from hexagon.domain.env import Env
from hexagon.domain import configuration
from hexagon.support.printer import log

_command_by_file_extension = {"js": "node", "sh": "bash"}


def execute_action(tool: Tool, env_args, env: Env, args):
    action_to_execute: str = tool.action
    ext = action_to_execute.split(".")[-1]
    script_action_command = (
        _command_by_file_extension[ext] if ext in _command_by_file_extension else None
    )

    if script_action_command:
        _execute_script(
            script_action_command, action_to_execute, env_args or [], env, args
        )
    else:
        python_module_found = _execute_python_module(
            action_to_execute, tool, env, env_args, args
        )
        if python_module_found:
            return

        split_action = action_to_execute.split(" ")
        return_code, executed_command = _execute_command(
            split_action[0],
            env_args,
            args,
            action_args=split_action[1:],
            handle_error=True,
        )

        if return_code != 0:
            if isinstance(return_code, int):
                log.error(f"{executed_command} returned {return_code}\n")
            elif return_code:
                log.error(f"{executed_command} failed with: {return_code}")
            else:
                log.error(f"{executed_command} failed")
            log.error("[dim] We tried looking for:")
            log.error(
                f"[dim]   - Your CLI's custom_tools_dir: [bold]{configuration.custom_tools_path}"
            )
            log.error(
                "[dim]   - Hexagon repository of externals tools (hexagon.tools.external)"
            )
            log.error("[dim]   - A known script file (.js, .sh)")
            log.error("[dim]   - Running your action as a shell command directly")
            sys.exit(1)


def _execute_python_module(action_id: str, tool: Tool, env: Env, env_args, args):
    tool_action_module = _load_action_module(action_id) or _load_action_module(
        f"hexagon.tools.external.{action_id}"
    )

    if not tool_action_module:
        return False
    try:
        tool_action_module.main(tool, env, env_args, args)
        return True
    except AttributeError as e:
        log.error(f"Execution of tool [bold]{action_id}[/bold] thru: {e}")
        log.error("Does it have the required `main(args...)` method?")
        sys.exit(1)


def _execute_command(
    command: str,
    env_args,
    cli_args,
    env: Env = None,
    action_args: List[str] = None,
    handle_error=False,
):
    action_args = action_args if action_args else []
    hexagon_args = __sanitize_args_for_command(env_args, env, *cli_args)
    command_to_execute = [command] + action_args + hexagon_args
    command_to_execute_as_string = " ".join(command_to_execute)

    def run():
        return subprocess.call(command_to_execute), command_to_execute_as_string

    if handle_error:
        try:
            return run()
        except Exception as error:
            return str(error), command_to_execute_as_string

    return run()


def _execute_script(command: str, script: str, env_args, env: Env, args):
    # Script should be relative to the project path
    script_path = os.path.join(configuration.project_path, script)
    if env and env.alias:
        del env.alias
    _execute_command(command, env_args, args, env, [script_path])


def __sanitize_args_for_command(*args: Union[List[any], Dict, Env]):
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


def _load_action_module(action_id: str):
    try:
        return __load_module(action_id)
    except ModuleNotFoundError:
        return None


def __load_module(module: str):
    if module in sys.modules:
        return sys.modules[module]

    return importlib.import_module(module)

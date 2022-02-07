import importlib
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import List, Union, Dict

from rich import traceback as rich_traceback

from hexagon.domain import configuration
from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.domain.tool.execution import ToolExecutionData
from hexagon.support.hooks import HexagonHooks
from hexagon.support.printer import log

_command_by_file_extension = {"js": "node", "sh": "sh"}


# TODO: use a decorator?
def execute_action(tool: ActionTool, env_args, env: Env, args, custom_tools_path=None):
    start = time.time()
    _execute_action(tool, env_args, env, args, custom_tools_path)
    HexagonHooks.tool_executed.run(
        ToolExecutionData(tool=tool, duration=(time.time() - start))
    )


def _execute_action(tool: ActionTool, env_args, env: Env, args, custom_tools_path=None):
    custom_tools_path = (
        custom_tools_path if custom_tools_path else configuration.custom_tools_path
    )
    action_to_execute: str = tool.action
    ext = action_to_execute.split(".")[-1]
    script_action_command = _command_by_file_extension.get(ext)

    if script_action_command:
        _execute_script(
            script_action_command, action_to_execute, env_args or [], env, args
        )
    else:
        python_module_found = _execute_python_module(
            action_to_execute, tool, env, env_args, args, custom_tools_path
        )
        if python_module_found:
            return

        split_action = action_to_execute.split(" ")
        return_code, executed_command = _execute_command(
            split_action[0], env_args, args, action_args=split_action[1:]
        )

        if return_code != 0:
            # "{executed_command} returned code: {return_code}\n"
            log.error(
                _("error.support.execute.action.command_result_code").format(
                    executed_command=executed_command, return_code=return_code
                )
            )

            if return_code == 127:
                log.error(
                    "{} [bold]{}".format(
                        _("error.support.execute.action.could_not_execute"), tool.action
                    )
                )
                log.error(_("error.support.execute.action.we_tried"))
                log.error(
                    "  - {} [bold]{}".format(
                        _("error.support.execute.action.attempt_cli_custom_dir"),
                        custom_tools_path,
                    )
                )
                log.error(
                    "  - {} (hexagon.actions.external)".format(
                        _("error.support.execute.action.attempt_internal_tools")
                    )
                )
                log.error(
                    "  - {} (.js, .sh)".format(
                        _("error.support.execute.action.attempt_known_script")
                    )
                )
                log.error(
                    "  - {}".format(
                        _("error.support.execute.action.attempt_inline_command")
                    )
                )
            sys.exit(1)


def _execute_python_module(
    action_id: str, tool: ActionTool, env: Env, env_args, args, custom_tools_path
):
    tool_action_module = _load_action_module(
        action_id, custom_tools_path
    ) or _load_action_module(f"hexagon.actions.external.{action_id}", custom_tools_path)

    if not tool_action_module:
        return False

    # noinspection PyBroadException
    try:
        tool_action_module.main(tool, env, env_args, args)
        return True
    except Exception:
        __pretty_print_external_error(action_id, custom_tools_path)
        log.error(
            _("error.support.execute.action.execute_tool_failed").format(
                action=action_id
            )
        )
        sys.exit(1)


def _execute_command(
    command: str, env_args, cli_args, env: Env = None, action_args: List[str] = None
):
    action_args = action_args if action_args else []
    hexagon_args = __sanitize_args_for_command(env_args, env, *cli_args)
    cmd_as_string = " ".join([command] + action_args + hexagon_args)

    return subprocess.call(cmd_as_string, shell=True), cmd_as_string


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
                positional.append(f'"{str(arg)}"')
    return named + positional


def _load_action_module(action_id: str, custom_tools_path):
    try:
        return __load_module(action_id)
    except ModuleNotFoundError as e:
        if e.name == action_id:
            return None
        else:
            __pretty_print_external_error(action_id, custom_tools_path)
            log.error(_("error.support.execute.action.python_dependency_error"))
            sys.exit(1)


def __load_module(module: str):
    if module in sys.modules:
        return sys.modules[module]

    return importlib.import_module(module)


def __pretty_print_external_error(action_id, custom_tools_path):
    exc_type, exc_value, tb = sys.exc_info()

    trace = __find_python_module_in_traceback(action_id, tb, custom_tools_path)

    if trace:
        log.example(
            rich_traceback.Traceback.from_exception(exc_type, exc_value, trace),
            decorator_start=False,
            decorator_end=False,
        )
    else:
        log.error(exc_value)


def __find_python_module_in_traceback(action_id, tb, custom_tools_path):
    return next(
        (
            t
            for t, path, file_name in __walk_tb(tb)
            if file_name == action_id
            or path == os.path.join(custom_tools_path, action_id)
        ),
        None,
    )


def __walk_tb(tb):
    def extract_metadata(_t):
        try:
            p = Path(traceback.extract_tb(_t)[0].filename)
            return p.parent, p.stem
        except IndexError:
            return None

    while tb is not None:
        path, file_name = extract_metadata(tb)
        yield tb, path.__str__(), file_name
        tb = tb.tb_next

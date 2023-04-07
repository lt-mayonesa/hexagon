import importlib
import os
import subprocess
import sys
from typing import List, Union, Dict, Any

from pydantic import ValidationError

from hexagon.domain.args import CliArgs, ToolArgs
from hexagon.domain.env import Env
from hexagon.domain.singletons import configuration
from hexagon.domain.tool import ActionTool
from hexagon.support.execute.errors import (
    ToolExecutionError,
    ActionInputError,
    ActionExecuteError,
    ActionImportError,
)
from hexagon.support.execute.execution_hook import execution_hook
from hexagon.support.parse_args import parse_cli_args
from hexagon.support.prompt import Prompt
from hexagon.support.tracer import tracer

ENVVAR_EXECUTION_ENV = "HEXAGON_EXECUTION_ENV"

ENVVAR_EXECUTION_TOOL = "HEXAGON_EXECUTION_TOOL"

TOOL_ARGUMENTS_CLASS_NAME = "Args"

_command_by_file_extension = {"js": "node", "sh": "sh"}


@execution_hook()
def execute_action(tool: ActionTool, env_args: Any, env: Env, cli_args: CliArgs):
    custom_tools_path = configuration.custom_tools_path
    action_to_execute: str = tool.executable_str
    script_action_command = __script_action_command(action_to_execute)

    if script_action_command:
        _execute_script(
            script_action_command,
            action_to_execute,
            env_args or [],
            tool,
            env,
            cli_args.raw_extra_args,
        )
    else:
        python_module_found = _execute_python_module(
            action_to_execute,
            tool,
            env,
            env_args,
            cli_args,
            custom_tools_path,
        )
        if python_module_found:
            return

        split_action = action_to_execute.split(" ")
        return_code, executed_command = _execute_command(
            split_action[0],
            env_args,
            cli_args.raw_extra_args,
            tool,
            env,
            action_args=split_action[1:],
        )

        if return_code != 0:
            raise ToolExecutionError(
                return_code, executed_command, tool.executable_str, custom_tools_path
            )


def __script_action_command(action_to_execute):
    ext = action_to_execute.split(".")[-1]
    script_action_command = _command_by_file_extension.get(ext)
    return script_action_command


def _execute_python_module(
    action_id: str, tool: ActionTool, env: Env, env_args, cli_args, custom_tools_path
):
    tool_action_module = _load_action_module(
        action_id, custom_tools_path
    ) or _load_action_module(f"hexagon.actions.external.{action_id}", custom_tools_path)

    if not tool_action_module:
        return False

    # noinspection PyBroadException
    try:
        tool_args = __parse_tool_args(cli_args, env, tool, tool_action_module)
        tool_action_module.main(
            tool,
            env,
            env_args,
            tool_args
            if type(tool_args).__name__ == TOOL_ARGUMENTS_CLASS_NAME
            else tool_args.extra_args,
        )
        return True
    except ValidationError as e:
        raise ActionInputError(e, tool.name)
    except Exception:
        raise ActionExecuteError(action_id, custom_tools_path)


def __parse_tool_args(cli_args, env, tool, tool_action_module):
    args = (
        [cli_args.env] if not env and cli_args.env else []
    ) + cli_args.raw_extra_args
    # noinspection PyProtectedMember
    return (
        parse_cli_args(
            args,
            tool_action_module.Args
            if hasattr(tool_action_module, TOOL_ARGUMENTS_CLASS_NAME)
            else ToolArgs,
            prog=tool.name,
            description=tool.description or tool.long_name or "Hexagon tool",
            add_help=True,
            epilog=_("msg.support.execute.action.tool_help_epilog"),
        )
        ._with_tracer(tracer())
        ._with_prompt(Prompt())
    )


def _execute_command(
    command: str,
    env_args,
    cli_args,
    tool: ActionTool,
    env: Env = None,
    action_args: List[str] = None,
):
    action_args = action_args if action_args else []
    hexagon_args = __sanitize_args_for_command(env_args, *cli_args)
    cmd_as_string = " ".join([command] + action_args + hexagon_args)

    env_vars = {
        ENVVAR_EXECUTION_TOOL: tool.json(),
    }
    if env:
        env_vars[ENVVAR_EXECUTION_ENV] = env.json()

    return (
        subprocess.call(cmd_as_string, shell=True, env=env_vars),
        cmd_as_string,
    )


def _execute_script(
    command: str, script: str, env_args, tool: ActionTool, env: Env, cli_args
):
    # Script should be relative to the project path
    script_path = os.path.join(configuration.project_path, script)
    _execute_command(command, env_args, cli_args, tool, env, [script_path])


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
    if not all(s and s.isidentifier() for s in action_id.split(".")):
        return None

    try:
        return __load_module(action_id)
    except ModuleNotFoundError as e:
        if e.name == action_id:
            return None
        else:
            raise ActionImportError(action_id, custom_tools_path)


def __load_module(module: str):
    if module in sys.modules:
        return sys.modules[module]

    return importlib.import_module(module)

import sys

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from hexagon.cli.args import fill_args
from hexagon.cli.tracer import tracer
from hexagon.cli.printer import log

from typing import Any, Dict, List


def main(
    tool: Dict[str, Any],
    env: Dict[str, Any] = None,
    env_args: Any = None,
    cli_args: List[Any] = None,
):
    """
    All hexagon tools must define a main function

    :param cli_args:
    :param env:
    :param tool:
    :param env_args: the values expected to receive from tool.envs
    :return:
    """

    # for now this is the way of obtaining other execution arguments (tool name, env name, etc)
    _, _tool_name, _env_name, _my_name = fill_args(sys.argv, 4)

    # tracer.tracing is the way of letting hexagon know you asked the user for a parameter for your tool.
    # this let's hexagon build the "To repeat this command" message correctly
    name = tracer.tracing(
        _my_name
        or inquirer.text(
            message="What's your last name?",
            validate=EmptyInputValidator("Please enter your last name."),
        ).execute()
    )

    log.info(f"Tool.action: {tool['action']}")
    log.info(f"Env: {env}")
    log.info(f"Valor en tool.envs: {env_args}")
    log.info(f"tu apellido es: {name}")

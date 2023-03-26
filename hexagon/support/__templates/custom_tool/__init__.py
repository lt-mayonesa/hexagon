from typing import Any, List, Optional

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.args import parse_cli_args, CliArgs
from hexagon.support.printer import log
from hexagon.support.tracer import tracer


def main(
    tool: ActionTool,
    env: Optional[Env] = None,
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
    args: CliArgs = parse_cli_args()

    # tracer.tracing is the way of letting hexagon know you asked the user for a parameter for your tool.
    # this lets hexagon build the "To repeat this command" message correctly
    name = tracer.tracing(
        args.extra_args["last-name"]
        or inquirer.text(
            message="What's your last name?",
            validate=EmptyInputValidator("Please enter your last name."),
        ).execute()
    )

    log.info(f"Tool.action: {tool.action}")
    log.info(f"Env: {env}")
    log.info(f"Valor en tool.envs: {env_args}")
    log.info(f"tu apellido es: {name}")

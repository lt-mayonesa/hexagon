from typing import Any, Optional, Dict

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.printer import log
from hexagon.support.tracer import tracer


def main(
    tool: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Dict[str, Any] = None,
):
    """
    All hexagon tools must define a main function

    :param tool: the ActionTool that is being executed, ie: all values present in the yaml
    :param env: the Env that is being executed, ie: all values present in the yaml
    :param env_args: the values expected to receive from tool.envs[env.name]
    :param cli_args: any extra arguments passed when executing hexagon, ie: --foo "bar"
    :return:
    """

    # tracer().tracing is the way of letting hexagon know you asked the user for a parameter for your tool.
    # this lets hexagon build the "To repeat this command" message correctly
    name = tracer().tracing(
        (cli_args and cli_args["last-name"])
        or inquirer.text(
            message="What's your last name?",
            validate=EmptyInputValidator("Please enter your last name."),
        ).execute()
    )

    log.info(f"selected tool: {tool.action}")
    log.info(f"selected env: {env}")
    log.info(f"values in tool.envs\\[env.name]: {env_args}")
    log.info(f"extra cli arguments: {cli_args}")
    log.result(f"your last name is: {name}")

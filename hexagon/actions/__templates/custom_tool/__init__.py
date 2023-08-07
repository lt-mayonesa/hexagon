from typing import Any, Optional

from pydantic import validator

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, Arg, OptionalArg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    last_name: OptionalArg[str] = Arg(
        None,
        prompt_message="What's your last name?",
    )

    @validator("last_name")
    def not_empty(cls, arg):
        if not arg.value:
            raise ValueError("Please enter your last name.")
        return arg


def main(
    tool: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    """
    All hexagon tools must define a main function

    :param tool: the ActionTool that is being executed, ie: all values present in the yaml
    :param env: the Env that is being executed, ie: all values present in the yaml
    :param env_args: the values expected to receive from tool.envs[env.name]
    :param cli_args: any extra arguments passed when executing hexagon, ie: --foo "bar"
    :return:
    """

    # the ideal way of asking the user for input is to use cli_args.prompt
    # this will make sure to trace the input accordingly
    if not cli_args.last_name:
        cli_args.last_name.prompt()

    log.info(f"selected tool: {tool.action}")
    log.info(f"selected env: {env}")
    log.info(f"values in tool.envs\\[env.name]: {env_args}")
    log.info(f"extra cli arguments: {cli_args}")
    log.result(f"your last name is: {cli_args.last_name}")

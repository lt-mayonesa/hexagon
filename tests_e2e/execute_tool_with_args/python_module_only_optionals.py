from typing import Any, Optional, List

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed loaded automatically by hexagon
    """

    name: OptionalArg[str]
    age: OptionalArg[str]
    country: OptionalArg[str]
    likes: OptionalArg[List[str]]


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"name: {cli_args.name.value}")
    log.result(f"age: {cli_args.age.value}")
    log.result(f"country: {cli_args.country.value}")
    log.result(f"likes: {cli_args.likes.value}")

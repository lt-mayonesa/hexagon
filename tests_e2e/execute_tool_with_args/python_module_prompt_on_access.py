from typing import Any, Optional, List, Union

from hexagon.domain.args import ToolArgs, OptionalArg
from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.printer import log


class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed loaded automatically by hexagon
    """

    name: OptionalArg[str]
    age: OptionalArg[str]
    country: OptionalArg[Union[str, int]]
    likes: OptionalArg[List[str]]


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"name: {cli_args.name}")
    log.result(f"age: {cli_args.age}")
    log.result(f"country: {cli_args.country}")
    log.result(f"likes: {cli_args.likes}")

from typing import Any, List, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import Tool
from hexagon.support.input.args import ToolArgs, OptionalArg, PositionalArg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed loaded automatically by hexagon
    """

    name: PositionalArg[str] = None
    age: PositionalArg[str] = None
    country: OptionalArg[str] = None
    likes: OptionalArg[List[str]] = None


def main(
    action: Tool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    if not cli_args.name.value:
        cli_args.name.prompt()
    log.result(f"name: {cli_args.name.value}")
    if not cli_args.age.value:
        cli_args.age.prompt()
    log.result(f"age: {cli_args.age.value}")
    if not cli_args.country.value:
        cli_args.country.prompt()
    log.result(f"country: {cli_args.country.value}")
    if not cli_args.likes.value:
        cli_args.likes.prompt()
    log.result(f"likes: {cli_args.likes.value}")

from typing import Any, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, PositionalArg
from hexagon.support.output.printer import log


# noinspection PyMethodParameters
class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed and loaded automatically by hexagon
    """

    name: PositionalArg[str]


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"name: {cli_args.name.value}")
    log.result(f"name: {cli_args.name.value}")
    log.result(f"name: {cli_args.name.value}")
    log.result(f"name: {cli_args.name.value}")
    log.result(f"name: {cli_args.name.value}")
    log.result(f"name: {cli_args.name.value}")

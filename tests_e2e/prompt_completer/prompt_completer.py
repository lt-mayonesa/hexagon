from typing import Any, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, PositionalArg, Arg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed loaded automatically by hexagon
    """

    test: PositionalArg[str] = Arg(
        None,
        prompt_suggestions=["test1", "test2", "test3"],
    )


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"test: {cli_args.test.prompt()}")

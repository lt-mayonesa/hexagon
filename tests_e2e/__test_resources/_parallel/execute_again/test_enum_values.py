from enum import Enum
from typing import Any, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, PositionalArg
from hexagon.support.output.printer import log


class Test(Enum):
    MY_ENUM = "this_should_be_printed"


class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed loaded automatically by hexagon
    """

    test: PositionalArg[Test] = None


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"test: {cli_args.test.prompt()}")

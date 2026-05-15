from enum import Enum
from typing import Any, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg
from hexagon.support.output.printer import log


class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Args(ToolArgs):
    color: OptionalArg[Color] = None


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"color: {cli_args.color.prompt().value}")

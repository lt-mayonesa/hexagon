from typing import Any, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg, Arg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    name: OptionalArg[str] = Arg(None, prompt_message="Enter your name:")


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"Hello, {cli_args.name.prompt()}!")

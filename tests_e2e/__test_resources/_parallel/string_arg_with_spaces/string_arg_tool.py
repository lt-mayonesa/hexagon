from typing import Optional, Any

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg, Arg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    query: OptionalArg[str] = Arg(None, prompt_message="What query do you want to run?")


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"query: {cli_args.query and cli_args.query.value}")

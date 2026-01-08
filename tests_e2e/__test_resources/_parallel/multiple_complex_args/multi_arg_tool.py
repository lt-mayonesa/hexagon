from typing import Optional, Any

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg, Arg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    query: OptionalArg[str] = Arg(None, prompt_message="SQL query")
    url: OptionalArg[str] = Arg(None, prompt_message="URL")
    path: OptionalArg[str] = Arg(None, prompt_message="File path")
    config: OptionalArg[str] = Arg(None, prompt_message="Config JSON")


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"query: {cli_args.query and cli_args.query.value}")
    log.result(f"url: {cli_args.url and cli_args.url.value}")
    log.result(f"path: {cli_args.path and cli_args.path.value}")
    log.result(f"config: {cli_args.config and cli_args.config.value}")

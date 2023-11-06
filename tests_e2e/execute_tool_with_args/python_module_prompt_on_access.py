from typing import Any, Optional, List, Union

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed loaded automatically by hexagon
    """

    name: OptionalArg[str] = None
    age: OptionalArg[int] = None

    class Config:
        prompt_on_access = True


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    # if prompt_on_access is set to True, the prompt will be shown when accessing the value
    log.result(f"name: {cli_args.name}")
    log.result(f"age: {cli_args.age}")

    # if arg has already been accessed, subsequent prompt should work as expected
    log.result(f"age 2: {cli_args.age.prompt()}")

from typing import Any, List, Optional

# noinspection PyUnresolvedReferences
from hexagon.cli.env import Env

from hexagon.domain.tool import ActionTool


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: List[Any] = None,
):
    print(f"executed {action.action}")

    if env:
        print("Env:")
        print(env)

    if env_args:
        print("Env args:")
        print(env_args)

    if cli_args and len(cli_args) > 0:
        print("Cli args:")
        for cli_arg in cli_args:
            print(cli_arg)

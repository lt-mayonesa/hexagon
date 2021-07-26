from typing import Any, List, Optional

from hexagon.domain.tool import Tool
from hexagon.domain.env import Env


def main(
    action: Tool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: List[Any] = None,
):
    print(f"executed {action.action}")

    err = [][3]
    print(err)
    if env_args:
        print("Env args:")
        print(env_args)

    if cli_args and len(cli_args) > 0:
        print("Cli args:")
        for cli_arg in cli_args:
            print(cli_arg)

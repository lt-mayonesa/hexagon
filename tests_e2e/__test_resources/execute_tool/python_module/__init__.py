from typing import Any, Optional, Dict

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Dict[str, Any] = None,
):
    print(f"executed {action.action}")

    if env:
        print("Env:")
        print(env)

    if env_args:
        print("Env args:")
        print(env_args)

    if cli_args and len(cli_args.keys()) > 0:
        print("Cli args:")
        for _, val in cli_args.items():
            print(val)

from typing import Any, List, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import Tool


def main(
    action: Tool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: List[Any] = None,
):
    print(f"executed {action.action}")

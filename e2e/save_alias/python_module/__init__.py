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

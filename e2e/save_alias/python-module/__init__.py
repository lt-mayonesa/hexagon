from typing import Any, Dict, List


def main(
    action: Dict[str, Any],
    env: Dict[str, Any] = None,
    env_args: Any = None,
    cli_args: List[Any] = None,
):
    print(f"executed {action['action']}")

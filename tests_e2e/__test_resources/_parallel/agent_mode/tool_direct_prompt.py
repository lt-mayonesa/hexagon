"""
Tool that calls prompt methods directly on the `prompt` object instead of
going through ToolArgs.  This mirrors the pattern used in internal hexagon
tools such as hexagon/runtime/update/hexagon.py.
"""

from typing import Any, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.prompt import prompt
from hexagon.support.output.printer import log


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Any = None,
):
    if prompt.confirm("Do you want to continue?", default=True):
        log.result("proceeding")
    else:
        log.result("cancelled")

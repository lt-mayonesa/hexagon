"""
Tool that loads its choices at runtime and passes them to .prompt().

Simulates the pattern where the available options are fetched externally
(e.g. from a config file, API, or database) and not statically declared
on the field itself.
"""

from typing import Any, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    option: OptionalArg[str] = None


def _load_options():
    """Simulate loading choices from an external source."""
    return ["fast", "slow", "medium"]


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    available = _load_options()
    choice = cli_args.option.prompt(choices=available, searchable=True)
    log.result(f"option: {choice}")

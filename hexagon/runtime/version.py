from typing import List

from hexagon.domain.cli import Cli
from hexagon.domain.env import Env
from hexagon.domain.tool import Tool
from hexagon.support.output.printer import log

# this updates automatically https://python-semantic-release.readthedocs.io/en/latest/index.html
__version__ = "0.62.0"


def print_version(cli_config: Cli, tools: List[Tool], envs: List[Env]):
    """
    Print either the current installed version of hexagon python package or the version of the cli tool

    :param cli_config:
    :param tools:
    :param envs:
    :return:
    """
    if cli_config.name == "Hexagon":
        log.extra(f"Hexagon: {__version__}")
        return

from itertools import groupby
from typing import Dict

from hexagon.domain.env import Env
from hexagon.domain.tool import Tool
from hexagon.domain.cli import Cli
from hexagon.support.printer import log


def print_help(cli_config: Cli, tools: Dict[str, Tool], envs: Dict[str, Env]):
    """
    Print the command line help text based on the tools and envs in configuration yaml

    :param cli_config:
    :param tools:
    :param envs:
    :return:
    """
    if cli_config.name == "Hexagon":
        log.info("[bold]Hexagon", gap_end=1)
        log.info("You are executing Hexagon without an install.")
        log.info('To get started run hexagon\'s "Install Hexagon" tool')
        return

    log.info(f"[bold]{cli_config.name}", gap_end=1)

    log.info("[bold][u]Envs:")
    for k, v in envs.items():
        log.info(f'  {k + (" (" + v.alias + ")" if v.alias else "")}')

    log.info("[bold][u]Tools:", gap_start=2)

    def key_func(z):
        x, y = z
        return y.type

    data = sorted(tools.items(), key=key_func, reverse=True)

    for gk, g in groupby(data, key_func):
        log.info(f"[bold]{gk}:", gap_start=1)

        for k, v in g:
            log.info(
                f'  {k + (" (" + v.alias + ")" if v.alias else ""):<60}[dim]{v.long_name or ""}'
            )
            if v.description:
                log.info(f'  {"": <60}[dim]{v.description}', gap_end=1)

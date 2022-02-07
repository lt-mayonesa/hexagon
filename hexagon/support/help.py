from itertools import groupby
from typing import List

from hexagon.domain.cli import Cli
from hexagon.domain.env import Env
from hexagon.domain.tool import Tool
from hexagon.support.printer import log


def print_help(cli_config: Cli, tools: List[Tool], envs: List[Env]):
    """
    Print the command line help text based on the tools and envs in configuration yaml

    :param cli_config:
    :param tools:
    :param envs:
    :return:
    """
    if cli_config.name == "Hexagon":
        log.info("[bold]Hexagon", gap_end=1)
        log.info(_("msg.support.help.no_install"))
        log.info(_("msg.support.help.get_started"))
        return

    log.info(f"[bold]{cli_config.name}", gap_end=1)

    log.info("[bold][u]{}:".format(_("msg.global.envs")))
    for env in envs:
        log.info(
            f'  {env.name + (" (" + env.alias + ")" if env.alias else ""):<60}[dim]{env.long_name or ""}'
        )
        if env.description:
            # TODO: if env is the last one it should not print with gap
            # the same for tools
            log.info(f'  {"": <60}[dim]{env.description}', gap_end=1)

    log.info("[bold][u]{}:".format(_("msg.global.tools")), gap_start=2)

    data = sorted(tools, key=lambda t: t.type, reverse=True)

    for gk, g in groupby(data, lambda t: t.type):
        log.info(f"[bold]{gk}:", gap_start=1)

        for tool in g:
            log.info(
                f'  {tool.name + (" (" + tool.alias + ")" if tool.alias else ""):<60}[dim]{tool.long_name or ""}'
            )
            if tool.description:
                log.info(f'  {"": <60}[dim]{tool.description}', gap_end=1)

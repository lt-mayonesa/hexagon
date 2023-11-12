from itertools import groupby
from typing import List

from hexagon.domain.cli import Cli
from hexagon.domain.env import Env
from hexagon.domain.tool import Tool
from hexagon.support.output.printer import log


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

    log.info(f"[bold]{cli_config.name}")
    log.info(
        f"usage: {cli_config.command} \[tool] \[env] \[\[positional-tool-arg] \[--optional-tool-arg=123] ...]",
        gap_start=1,
        gap_end=1,
    )

    log.info(_("msg.support.help.envs"))
    for i, env in enumerate(envs):
        log.info(
            f'  {env.name + (" (" + env.alias + ")" if env.alias else ""):<60}[dim]{env.long_name or ""}'
        )
        if env.description:
            log.info(
                f'  {"": <60}[dim]{env.description}',
                gap_end=__gap_if_last(envs, i),
            )
        else:
            log.gap()

    log.info(_("msg.support.help.tools"), gap_start=1)

    data = sorted(tools, key=lambda t: t.type, reverse=True)

    for gk, g in groupby(data, lambda t: t.type):
        log.info(f"[bold]{gk}:", gap_start=1)
        type_tools = list(g)

        for i, tool in enumerate(type_tools):
            log.info(
                f'  {tool.name + (" (" + tool.alias + ")" if tool.alias else ""):<60}[dim]{tool.long_name or ""}'
            )
            if tool.description:
                log.info(
                    f'  {"": <60}[dim]{tool.description}',
                    gap_end=__gap_if_last(type_tools, i),
                )


def __gap_if_last(envs, i):
    return 1 if i + 1 < len(envs) else 0

import sys

from hexagon.support.args import fill_args
from hexagon.domain import cli, tools, envs
from hexagon.support.execute_tool import execute_action
from hexagon.support.help import print_help
from hexagon.support.tracer import tracer
from hexagon.support.wax import search_by_key_or_alias, select_env, select_tool
from hexagon.support.printer import log
from hexagon.support.storage import (
    HexagonStorageKeys,
    store_user_data,
)


def main():
    _, _tool, _env = fill_args(sys.argv, 3)

    if _tool == "-h" or _tool == "--help":
        return print_help(cli, tools, envs)

    log.start(f"[bold]{cli.name}")
    log.gap()

    if cli.name == "Hexagon":
        log.info(
            "This looks like your first time running Hexagon.",
            'You should probably run "Install CLI".',
            gap_end=1,
        )

    try:
        _tool = search_by_key_or_alias(tools, _tool)
        _env = search_by_key_or_alias(envs, _env)

        name, tool = select_tool(tools, _tool)
        tracer.tracing(name)

        env, params = select_env(envs, tool.envs, _env)
        tracer.tracing(env)

        action = execute_action(tool, params, envs.get(env, None), sys.argv[3:])

        log.gap()

        if action:
            for result in action:
                log.info(result)

        log.finish()

        if tracer.has_traced() and cli.command:
            log.extra(
                "[cyan dim]Para repetir este comando:[/cyan dim]",
                f"[cyan]     {cli.command} {tracer.command()}[/cyan]",
            )
            command_as_aliases = tracer.command_as_aliases(tools, envs)
            if command_as_aliases:
                log.extra(
                    "[cyan dim]  o:[/cyan dim]",
                    f"[cyan]     {cli.command} {command_as_aliases}[/cyan]",
                )
            store_user_data(
                HexagonStorageKeys.last_command.value,
                f"{cli.command} {tracer.command()}",
            )
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()

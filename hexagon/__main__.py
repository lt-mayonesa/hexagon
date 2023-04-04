import sys

from hexagon.plugins import collect_plugins
from hexagon.support.printer import log
from hexagon.support.storage import (
    HexagonStorageKeys,
    store_user_data,
)


def main():
    try:
        from hexagon.domain.singletons import cli, tools, envs, options, configuration
        from hexagon.support.execute.tool import select_and_execute_tool
        from hexagon.support.help import print_help
        from hexagon.support.hooks import HexagonHooks
        from hexagon.support.parse_args import parse_cli_args
        from hexagon.support.tracer import init_tracer
        from hexagon.support.update.cli import check_for_cli_updates
        from hexagon.support.update.hexagon import check_for_hexagon_updates

        log.load_theme(options.theme)

        args = parse_cli_args()

        if args.show_help:
            return print_help(cli, tools, envs)

        collect_plugins(configuration.project_path, cli.plugins_dir)
        tracer = init_tracer(args)

        HexagonHooks.start.run()
        log.start(f"[bold]{cli.name}")
        log.gap()

        check_for_hexagon_updates()

        if cli.name == "Hexagon":
            log.info(
                _("msg.main.first_time_intro"), _("msg.main.first_time_tool"), gap_end=1
            )
        else:
            check_for_cli_updates()

        result = select_and_execute_tool(tools, envs, args)

        log.gap()

        if result:
            for item in result:
                log.info(item)

        log.finish()

        tracer.print_run_again(cli.command, tools, envs, log)
        store_user_data(
            HexagonStorageKeys.last_command.value, f"{cli.command} {tracer.trace()}"
        )

        HexagonHooks.end.run()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        from hexagon.domain.hexagon_error import HexagonError

        if isinstance(e, HexagonError):
            e.print(log)
            sys.exit(e.exit_status)
        else:
            raise e


if __name__ == "__main__":
    main()

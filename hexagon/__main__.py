import sys

from rich import print

from hexagon.cli.args import fill_args
from hexagon.cli.config import init_config
from hexagon.cli.execute_tool import register_external_tools, execute_action
from hexagon.cli.help import print_help
from hexagon.cli.tracer import tracer
from hexagon.cli.wax import search_by_key_or_alias, select_env, select_tool


def main():
    _, _tool, _env = fill_args(sys.argv, 3)

    cli_config, tools, envs = init_config()

    register_external_tools(cli_config)

    if _tool == '-h' or _tool == '--help':
        return print_help(cli_config, tools, envs)

    print(f'╭╼ [bold]{cli_config["name"]}')
    print('│')

    if cli_config['name'] == 'Hexagon':
        print('│ This looks like your first time running Hexagon.')
        print('│ You should probably run "Install Hexagon".')
        print('│')

    try:
        _tool = search_by_key_or_alias(tools, _tool)
        _env = search_by_key_or_alias(envs, _env)

        name, tool = select_tool(tools, _tool)
        tracer.tracing(name)

        env, params = select_env(envs, tool['envs'] if 'envs' in tool else None, _env)
        tracer.tracing(env)

        action = execute_action(tool["action"], params)

        print('│')

        if action:
            for result in action:
                print(result)

        print('╰╼')

        if tracer.has_traced() and 'command' in cli_config:
            print('[cyan dim]Para repetir este comando:[/cyan dim]')
            print(f'[cyan]     {cli_config["command"]} {tracer.command()}[/cyan]')
            print('[cyan dim]  o:[/cyan dim]')
            print(f'[cyan]     {cli_config["command"]} {tracer.command_as_aliases(tools, envs)}[/cyan]')
            dump = open('last_command', 'w')
            dump.write(f'{cli_config["command"]} {tracer.command()}')
            dump.close()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    main()

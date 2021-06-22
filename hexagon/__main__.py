import sys

from rich import print

from hexagon.cli.args import fill_args
from hexagon.cli.config import cli, tools, envs
from hexagon.cli.execute_tool import register_external_tools, execute_action
from hexagon.cli.help import print_help
from hexagon.cli.tracer import tracer
from hexagon.cli.wax import search_by_key_or_alias, select_env, select_tool


def main():
    _, _tool, _env = fill_args(sys.argv, 3)

    register_external_tools()

    if _tool == '-h' or _tool == '--help':
        return print_help(cli, tools, envs)

    print(f'╭╼ [bold]{cli["name"]}')
    print('│')

    if cli['name'] == 'Hexagon':
        print('│ This looks like your first time running Hexagon.')
        print('│ You should probably run "Install CLI".')
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

        if tracer.has_traced() and 'command' in cli:
            print('[cyan dim]Para repetir este comando:[/cyan dim]')
            print(f'[cyan]     {cli["command"]} {tracer.command()}[/cyan]')
            command_as_aliases = tracer.command_as_aliases(tools, envs)
            if command_as_aliases:
                print('[cyan dim]  o:[/cyan dim]')
                print(f'[cyan]     {cli["command"]} {command_as_aliases}[/cyan]')
            dump = open('last_command', 'w')
            dump.write(f'{cli["command"]} {tracer.command()}')
            dump.close()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    main()

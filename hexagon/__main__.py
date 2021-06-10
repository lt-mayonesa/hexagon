import sys

from rich import print

from hexagon.cli.args import fill_args
from hexagon.cli.config import init_config
from hexagon.cli.help import print_help
from hexagon.cli.tracer import tracer
from hexagon.cli.wax import key_or_alias, select_env, select_tool
from hexagon.tools.bastion import bastion
from hexagon.tools.docker_registry import docker_registry
from hexagon.tools.install_hexagon import install_hexagon
from hexagon.tools.open_link import open_link
from hexagon.tools.save_new_alias import save_new_alias

ACTIONS = {
    'save_new_alias': save_new_alias,
    'install_hexagon': install_hexagon,
    'open_link': open_link,
    'bastion': bastion,
    'docker_registry': docker_registry
}


def main():
    _, _tool, _env = fill_args(sys.argv, 3)

    cli_config, tools, envs = init_config()

    if _tool == '-h' or _tool == '--help':
        return print_help(cli_config, tools, envs)

    print(f'╭╼ [bold]{cli_config["name"]}')
    print('│')

    if cli_config['name'] == 'Hexagon':
        print('│ This looks like your first time running Hexagon.')
        print('│ You should probably run "Install Hexagon".')
        print('│')

    _tool = key_or_alias(tools, _tool)
    _env = key_or_alias(envs, _env)

    name, tool = select_tool(tools, _tool)
    tracer.tracing(name)

    env, params = select_env(envs, tool['envs'] if 'envs' in tool else None, _env)
    tracer.tracing(env)

    action = ACTIONS[tool['action']](params)

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


if __name__ == '__main__':
    main()

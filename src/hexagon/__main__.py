import os
import sys

import yaml
from hexagon.cli.args import fill_args
from hexagon.cli.tracer import tracer
from hexagon.cli.wax import key_or_alias, select_env, select_tool
from hexagon.tools.bastion import bastion
from hexagon.tools.docker_registry import docker_registry
from hexagon.tools.install_hexagon import install_hexagon
from hexagon.tools.open_link import open_link
from hexagon.tools.save_new_alias import save_new_alias
from rich import print

with open(os.getenv('HEXAGON_CONFIG_FILE', 'app.yaml'), 'r') as f:
    __config = yaml.load(f, Loader=yaml.CLoader)

TOOLS = {
    **__config['tools'],
    **{
        'save-alias': {
            'alias': 'sa',
            'long_name': 'Save OS Alias',
            'type': 'hexagon',
            'envs': {
                '*': None
            },
            'action': 'save_new_alias'
        },
        'install': {
            'long_name': 'Install Hexagon',
            'type': 'hexagon',
            'envs': {
                '*': None
            },
            'action': 'install_hexagon'
        }
    }
}

ENVS = __config['envs']

ACTIONS = {
    'save_new_alias': save_new_alias,
    'install_hexagon': install_hexagon,
    'open_link': open_link,
    'bastion': bastion,
    'docker_registry': docker_registry
}


def main():
    _, _tool, _env = fill_args(sys.argv, 3)

    if _tool == '-h' or _tool == '--help':
        return print_help()

    print(f'╭╼ [bold]{__config["cli"]["name"]}')
    print('│')

    _tool = key_or_alias(TOOLS, _tool)
    _env = key_or_alias(ENVS, _env)

    name, tool = select_tool(TOOLS, _tool)
    tracer.tracing(name)

    env, params = select_env(ENVS, tool['envs'], _env)
    tracer.tracing(env)

    action = ACTIONS[tool['action']](params)

    print('│')

    if action:
        for result in action:
            print(result)

    print('╰╼')

    if tracer.has_traced():
        print('[cyan dim]Para repetir este comando:[/cyan dim]')
        print(f'[cyan]     {__config["cli"]["command"]} {tracer.command()}[/cyan]')
        print('[cyan dim]  o:[/cyan dim]')
        print(f'[cyan]     {__config["cli"]["command"]} {tracer.command_as_aliases(TOOLS, ENVS)}[/cyan]')
        dump = open('last_command', 'w')
        dump.write(f'{__config["cli"]["command"]} {tracer.command()}')
        dump.close()


def print_help():
    print('│   [bold]Todo Pago CLI')
    print('│')
    for k, v in TOOLS.items():
        print(f'│   {k + " (" + v["alias"] + ")":<60}[dim]{v["long_name"]}')
        if "description" in v:
            print(f'│   {"": <60}[dim]{v["description"]}')
            print('│')


if __name__ == '__main__':
    main()

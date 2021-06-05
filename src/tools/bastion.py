import clipboard
import requests
from InquirerPy import inquirer
from rich import print

from src.cli.args import fill_args
from src.cli.tracer import tracer


def bastion(bastion_env_name):
    _, _tool, _env, _query = fill_args(4)

    def choice(e):
        name = e[1].replace(".marathon.l4lb.thisdcos.directory", "")
        url = f'http://bastion.prisma.redbee.io:{e[0]}'
        val = f'{name}={url}'
        serv = f'{name}:{e[2]}'
        return {
            'value': val,
            'name': f'{serv: <60}{url}'
        }

    def get_services():
        x = requests.get('http://bastion.prisma.redbee.io:9999/tuneles?name=' + bastion_env_name)
        x = x.text[x.text.index('</h1>') + 5:]
        x = x.split('<br>')
        return [choice(e.split(':')) for e in x]

    v, u = inquirer.fuzzy(
        message="¿Qué componente estás buscando?",
        choices=lambda _: get_services(),
        default=_query,
        validate=lambda c: c,
        transformer=lambda r: r.split(':')[:1][0],
        filter=lambda r: r.split('=')
    ).execute()

    tracer.tracing(v)
    clipboard.copy(f'{u}')
    print(f'├ [dim][u]{u}[/u] se copió al portapapeles')

    return []

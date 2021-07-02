import json
import os

import clipboard
import requests
from InquirerPy import inquirer

from hexagon.cli.args import cli_arg
from hexagon.cli.tracer import tracer
from hexagon.cli.printer import log


def main(tool, env, env_args, cli_args):
    registry_host = env_args
    _image = cli_arg(cli_args, 0)
    _filter = cli_arg(cli_args, 1)

    with open(os.path.expanduser("~/.docker/config.json")) as config:
        auth = json.load(config)["auths"][registry_host]["auth"]

    def get_authenticated(_url, j_path=None):
        __x = requests.get(_url, headers={"Authorization": f"Basic {auth}"}).json()
        return __x[j_path] if j_path else __x

    image = tracer.tracing(
        _image
        or inquirer.fuzzy(
            message="¿Qué imagen estás buscando?",
            choices=lambda _: get_authenticated(
                f"https://{registry_host}/v2/_catalog", "repositories"
            ),
        ).execute()
    )

    tag = tracer.tracing(
        _filter
        or inquirer.fuzzy(
            message="¿Qué tag?",
            choices=lambda _: get_authenticated(
                f"https://{registry_host}/v2/{image}/tags/list", "tags"
            ),
        ).execute()
    )

    clipboard.copy(f"{registry_host}/{image}:{tag}")
    log.result(f"[dim][u]{registry_host}/{image}:{tag}[/u] se copió al portapapeles")

    manifest = inquirer.confirm(
        message="¿Te gustaría ver el manifest?", default=False
    ).execute()

    if manifest:
        x = get_authenticated(f"https://{registry_host}/v2/{image}/manifests/{tag}")
        return [x]

    return []

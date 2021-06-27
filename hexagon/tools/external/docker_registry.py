import json
import os
import sys

import clipboard
import requests
from InquirerPy import inquirer
from rich import print

from hexagon.cli.args import fill_args
from hexagon.cli.tracer import tracer


def main(registry_host):
    _, _tool, _env, _image, _filter = fill_args(sys.argv, 5)

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
    print(f"├ [dim][u]{registry_host}/{image}:{tag}[/u] se copió al portapapeles")

    manifest = inquirer.confirm(
        message="¿Te gustaría ver el manifest?", default=False
    ).execute()

    if manifest:
        x = get_authenticated(f"https://{registry_host}/v2/{image}/manifests/{tag}")
        return [x]

    return []

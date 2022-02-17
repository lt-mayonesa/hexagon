import json
import os

import clipboard
import requests
from InquirerPy import inquirer

from hexagon.support.args import cli_arg
from hexagon.support.printer import log
from hexagon.support.tracer import tracer


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
            message=_("action.actions.external.docker_registry.prompt_docker_image"),
            choices=lambda _: get_authenticated(
                f"https://{registry_host}/v2/_catalog", "repositories"
            ),
        ).execute()
    )

    tag = tracer.tracing(
        _filter
        or inquirer.fuzzy(
            message=_("action.actions.external.docker_registry.prompt_tag"),
            choices=lambda _: get_authenticated(
                f"https://{registry_host}/v2/{image}/tags/list", "tags"
            ),
        ).execute()
    )

    clipboard.copy(f"{registry_host}/{image}:{tag}")
    log.result(
        _("msg.actions.external.docker_registry.copied_to_clipboard").format(
            host=registry_host, image=image, tag=tag
        )
    )

    manifest = inquirer.confirm(
        message=_("action.actions.external.docker_registry.confirm_see_manifest"),
        default=False,
    ).execute()

    if manifest:
        x = get_authenticated(f"https://{registry_host}/v2/{image}/manifests/{tag}")
        return [x]

    return []

from typing import Any, Dict, List

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from hexagon.cli.tracer import tracer
from hexagon.cli.printer import log
from hexagon.cli.args import cli_arg


# Toda tool de hexagon tiene que tener un main que se va a invocar
# Los argumentos que se reciben son, en orden:
#   tool: La tool por la cual se ejecuto este modulo
#   env: El entorno indicado por el usuario
#   env_args: Los argumentos deifnidos para el entorno
#   cli_args: Otros argumentos que indico el usuario por CLI


def main(
    tool: Dict[str, Any],
    env: Dict[str, Any] = None,
    env_args: Any = None,
    cli_args: List[Any] = None,
):
    _name = cli_arg(cli_args, 0)

    # Es importante usar tracer.tracing para registrar los argumentos/sub_comandos que
    # se van ejecutando. de está manera hexagon puede recomendar al usuario
    # la manera de repetir el comando nuevamente sin prompts.
    name = tracer.tracing(
        _name
        or inquirer.text(
            message="¿Cómo es tu apellido?",
            validate=EmptyInputValidator("Poneme un apellido válido, por favor."),
        ).execute()
    )

    log.info(f"Tool.action: {tool['action']}")
    log.info(f"Env: {env}")
    log.info(f"Valor en tool.envs: {env_args}")
    log.info(f"tu apellido es: {name}")

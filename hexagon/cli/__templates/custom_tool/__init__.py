import sys

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from hexagon.cli.args import fill_args
from hexagon.cli.tracer import tracer
from hexagon.cli.printer import log


# Toda tool de hexagon tiene que tener un main que se va a invocar
# con los valores el objeto envs, si es que existe.


def main(env_values):
    # por ahora está es la forma de obtener los argumentos de ejecución del comando
    # cada script de tool se encarga de definir que representa cada argumento en base a su posición.
    #
    # _ es el nombre del script (hexagon/__main__.py) y dependiendo del OS puede tener path
    # _tool (si existe) siempre va a ser el segundo argumento
    # _env (si existe) siempre va a ser el tercer argumento
    _, _tool, _env, _name = fill_args(sys.argv, 4)

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

    log.info("Valor en tool.envs:", env_values)
    log.info("tu apellido es:", name)

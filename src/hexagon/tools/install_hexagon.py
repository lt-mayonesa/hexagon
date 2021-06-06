from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from hexagon.tools.save_new_alias import save_new_alias


def install_hexagon(_):
    src_path = inquirer.filepath(
        message="Indicá el archivo de configuración",
        default=str(Path.cwd()),
        validate=PathValidator(is_file=True, message="No es un archivo"),
        only_files=True,
    ).execute()

    save_new_alias(None, name='tp', command=f'HEXAGON_CONFIG_FILE={src_path} hexagon')

import os

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from rich import print


def save_new_alias(_):
    shell_ = os.environ['SHELL']

    shell_aliases = {
        '/usr/bin/zsh': f'{os.environ["HOME"]}/.oh-my-zsh/custom/aliases.zsh',
        '/usr/bin/bash': f'{os.environ["HOME"]}/.bash_aliases'
    }

    with open('last_command', 'r') as f:
        last_command = f.read()

    alias_name = inquirer.text(
        message=f"Ultimo comando: {last_command} ¿Qué alias querés crear?",
        validate=EmptyInputValidator("Es necesario ingresar un alias")
    ).execute()

    with open(shell_aliases[shell_], 'r+') as aliases_file:
        print(aliases_file.read())
        aliases_file.write(
            '\n'
            '# added by hexagon\n'
            f'alias {alias_name}="{last_command}"'
        )
        aliases_file.seek(0)
        print(aliases_file.read())
        aliases_file.close()

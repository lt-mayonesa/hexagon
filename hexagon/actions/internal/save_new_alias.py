import os
import subprocess

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from hexagon.support.printer import log
from hexagon.support.storage import (
    HexagonStorageKeys,
    load_user_data,
)


def main(*_):
    last_command = load_user_data(HexagonStorageKeys.last_command.value)

    alias_name = inquirer.text(
        message=f"Last command: {last_command} Alias name?",
        validate=EmptyInputValidator("Please insert a valid unix alias."),
    ).execute()

    save_new_alias(alias_name, last_command)


def save_new_alias(alias_name, command):
    shell_ = (
        os.environ["HEXAGON_TEST_SHELL"]
        if "HEXAGON_TEST_SHELL" in os.environ
        else os.environ["SHELL"]
    )

    shell_aliases = {
        "/usr/bin/zsh": f'{os.environ["HOME"]}/.oh-my-zsh/custom/aliases.zsh',
        "/bin/zsh": f'{os.environ["HOME"]}/.oh-my-zsh/custom/aliases.zsh',
        "/usr/bin/bash": f'{os.environ["HOME"]}/.bash_aliases',
        "/bin/bash": f'{os.environ["HOME"]}/.bash_aliases',
        "HEXAGON_TEST_SHELL": "home-aliases.txt",
    }

    aliases_file_path = shell_aliases[shell_]

    with open(aliases_file_path, "a+") as aliases_file:
        aliases_file.write(
            "\n" "# added by hexagon\n" f'alias {alias_name}="{command}"'
        )
        aliases_file.seek(0)
        __pretty_print_created_alias(aliases_file, aliases_file_path, lines_to_show=-3)
        aliases_file.close()

    if shell_ != "HEXAGON_TEST_SHELL":
        subprocess.call([shell_, "-c", f"source {aliases_file_path}"])
    log.info("[u]All done! Now you can execute your project's CLI like:", gap_end=1)
    log.result(f"[b]$ {alias_name}")


def __pretty_print_created_alias(aliases_file, file, lines_to_show=-10):
    log.gap()
    log.info(f"Added alias to {file}")
    log.example("\n".join(aliases_file.read().splitlines()[lines_to_show:]))

import os

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from hexagon.support.printer import log
from hexagon.support.storage import (
    HexagonStorageKeys,
    load_user_data,
)


def main(*__):
    last_command = load_user_data(HexagonStorageKeys.last_command.value)

    log.info(
        _("msg.actions.internal.save_new_alias.last_command").format(
            last_command=last_command
        )
    )

    alias_name = inquirer.text(
        message=_("action.actions.internal.save_new_alias.prompt_alias_name"),
        validate=EmptyInputValidator(
            _("error.actions.internal.save_new_alias.insert_valid_alias")
        ),
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

    log.info(
        _("msg.actions.internal.save_new_alias.success"), gap_end=1,
    )
    log.result(f"[b]$ {alias_name}")
    log.info(
        _("msg.actions.internal.save_new_alias.execute_tip"), gap_start=1,
    )
    log.info(_("msg.actions.internal.save_new_alias.reload_builtins"))
    log.info(
        _("msg.actions.internal.save_new_alias.run_source").format(
            file_path=aliases_file_path
        )
    )


def __pretty_print_created_alias(aliases_file, file, lines_to_show=-10):
    log.gap()
    log.info(_("msg.actions.internal.save_new_alias.added_to_file").format(file=file))
    log.example("\n".join(aliases_file.read().splitlines()[lines_to_show:]))

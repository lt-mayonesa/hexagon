import os
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from prompt_toolkit.validation import ValidationError

from hexagon.domain import configuration
from hexagon.support.printer import log
from hexagon.support.dependencies import scan_and_install_dependencies
from hexagon.support.storage import load_user_data, HexagonStorageKeys, store_user_data


class YamlFileValidator(PathValidator):
    def validate(self, document) -> None:
        super(YamlFileValidator, self).validate(document)
        extension = document.text.split("/")[-1].split(".")[-1]
        if extension != "yaml" and extension != "yml":
            raise ValidationError(
                message=self.message, cursor_position=document.cursor_position
            )


def main(*__):
    src_path = inquirer.filepath(
        message=_("action.actions.internal.install_cli.config_file_location"),
        default=str(Path.cwd()),
        validate=YamlFileValidator(
            is_file=True,
            message=_("error.actions.internal.install_cli.select_valid_file"),
        ),
    ).execute()

    cli, tools, envs = configuration.init_config(src_path)

    bin_path = load_user_data(HexagonStorageKeys.cli_install_path.value)

    if not bin_path:
        bin_path = inquirer.filepath(
            message=_("action.actions.internal.install_cli.commands_path"),
            default=str(os.path.expanduser(os.path.join("~", "bin"))),
            validate=PathValidator(
                is_dir=True,
                message=_("error.actions.internal.install_cli.select_valid_directory"),
            ),
        ).execute()
        store_user_data(HexagonStorageKeys.cli_install_path.value, bin_path)

    command_path = os.path.join(bin_path, cli.command)
    with open(command_path, "w") as command:
        command.write(
            "#!/bin/bash\n"
            "# file create by hexagon\n"
            f"HEXAGON_CONFIG_FILE={src_path} hexagon $@"
        )

    _make_executable(command_path)
    scan_and_install_dependencies(cli.custom_tools_dir)

    log.info(
        _("msg.actions.internal.install_cli.success"),
        gap_end=1,
        gap_start=1,
    )
    log.result(f"[b]$ {cli.command}")

    path = os.getenv("PATH").split(":")

    if bin_path not in path:
        log.info(
            _("msg.actions.internal.install_cli.not_in_path").format(dir=bin_path),
            gap_start=1,
        )


def _make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)

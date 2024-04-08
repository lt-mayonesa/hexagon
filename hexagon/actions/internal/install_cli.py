import os
from pathlib import Path

from pydantic import FilePath, validator, DirectoryPath

from hexagon.runtime.dependencies import scan_and_install_dependencies
from hexagon.runtime.singletons import configuration
from hexagon.support.input.args import ToolArgs, Arg, PositionalArg, OptionalArg
from hexagon.support.output.printer import log
from hexagon.support.storage import (
    load_user_data,
    HexagonStorageKeys,
    store_user_data,
)


class Args(ToolArgs):
    src_path: PositionalArg[FilePath] = Arg(
        None,
        prompt_message=_("action.actions.internal.install_cli.config_file_location"),
    )
    bin_path: OptionalArg[DirectoryPath] = Arg(
        None,
        prompt_message=_("action.actions.internal.install_cli.commands_path"),
        prompt_default=str(os.path.expanduser(os.path.join("~", ".local", "bin"))),
    )

    @validator("src_path")
    def is_yaml(cls, arg):
        if isinstance(arg, str):
            if arg.endswith(".yaml") or arg.endswith(".yml"):
                return arg
        else:
            if arg.value.suffix == ".yaml" or arg.value.suffix == ".yml":
                return arg
        raise ValueError(_("error.actions.internal.install_cli.select_valid_file"))


def main(_tool, _env, _env_args, cli_args: Args):
    if not cli_args.src_path.value:
        cli_args.src_path.prompt(default=str(Path.cwd()))

    cli, tools, envs = configuration.init_config(cli_args.src_path.value.resolve())

    bin_path = (
        load_user_data(HexagonStorageKeys.cli_install_path.value)
        or cli_args.bin_path.value
    )

    if not bin_path:
        if not cli_args.bin_path.value:
            bin_path = cli_args.bin_path.prompt().resolve()
        store_user_data(HexagonStorageKeys.cli_install_path.value, str(bin_path))

    command_path = os.path.join(bin_path, cli.command)
    with open(command_path, "w") as command:
        command.write(
            "#!/bin/bash\n"
            "# file create by hexagon\n"
            f"HEXAGON_CONFIG_FILE={cli_args.src_path.value.resolve()} hexagon $@"
        )

    _make_executable(command_path)
    scan_and_install_dependencies(configuration.custom_tools_path)

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

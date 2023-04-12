import os
from pathlib import Path

from pydantic import FilePath, validator, DirectoryPath

from hexagon.domain.args import ToolArgs, Arg, PositionalArg
from hexagon.domain.singletons import configuration
from hexagon.support.dependencies import scan_and_install_dependencies
from hexagon.support.printer import log
from hexagon.support.storage import load_user_data, HexagonStorageKeys, store_user_data


class Args(ToolArgs):
    src_path: PositionalArg[FilePath] = Arg(
        str(Path.cwd()),
        prompt_message=_("action.actions.internal.install_cli.config_file_location"),
    )
    bin_path: PositionalArg[DirectoryPath] = Arg(
        str(os.path.expanduser(os.path.join("~", "bin"))),
        prompt_message=_("action.actions.internal.install_cli.commands_path"),
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


def main(tool, env, env_args, cli_args: Args):
    cli_args.prompt("src_path")

    cli, tools, envs = configuration.init_config(cli_args.src_path.value.resolve())

    bin_path = load_user_data(HexagonStorageKeys.cli_install_path.value)

    if not bin_path:
        bin_path = cli_args.prompt("bin_path").resolve()
        store_user_data(HexagonStorageKeys.cli_install_path.value, bin_path)

    command_path = os.path.join(bin_path, cli.command)
    with open(command_path, "w") as command:
        command.write(
            "#!/bin/bash\n"
            "# file create by hexagon\n"
            f"HEXAGON_CONFIG_FILE={cli_args.src_path.value.resolve()} hexagon $@"
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

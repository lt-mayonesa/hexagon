import os
import re
from pathlib import Path
from typing import List

from hexagon.domain.cli import Cli
from hexagon.domain.env import Env
from hexagon.runtime.configuration import ConfigFile
from hexagon.runtime.yaml import write_file
from hexagon.support.input.args import ToolArgs, Arg, PositionalArg, OptionalArg
from hexagon.support.input.prompt import prompt
from hexagon.support.output.printer import log


class Args(ToolArgs):
    dir_name: PositionalArg[str] = Arg(
        None,
        prompt_default="my-team-tools",
        prompt_message=_("action.actions.internal.create_cli.directory_name"),
    )
    title: OptionalArg[str] = Arg(
        None,
        prompt_default="My Team CLI",
        prompt_message=_("action.actions.internal.create_cli.title"),
    )
    command: OptionalArg[str] = Arg(
        None,
        prompt_message=_("action.actions.internal.create_cli.command"),
    )
    environments: OptionalArg[List[str]] = Arg(
        None,
        prompt_message=_("action.actions.internal.create_cli.environments"),
    )


def main(_tool, _env, _env_args, cli_args: Args):
    ensure_directory_exists(cli_args)
    ensure_required_inputs_provided(cli_args)
    environments = create_environments_from_input(cli_args.environments.value)
    config_path = create_config_file(cli_args, environments)
    display_success_message(cli_args, config_path)


def ensure_directory_exists(cli_args: Args) -> Path:
    if not cli_args.dir_name.value:
        cli_args.dir_name.prompt()

    dir_path = Path(cli_args.dir_name.value).resolve()
    if should_abort_for_non_empty_directory(dir_path):
        log.info(_("msg.actions.internal.create_cli.directory_not_empty_cancelled"))
        return

    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def should_abort_for_non_empty_directory(dir_path: Path) -> bool:
    if dir_path.exists() and any(dir_path.iterdir()):
        return not prompt.confirm(
            _("action.actions.internal.create_cli.directory_not_empty").format(
                dir_name=dir_path
            )
        )
    return False


def ensure_required_inputs_provided(cli_args: Args) -> None:
    if not cli_args.title.value:
        cli_args.title.prompt()

    if not cli_args.command.value:
        default_command = generate_command_from_title(cli_args.title.value)
        cli_args.command.prompt(default=default_command)

    if not cli_args.environments.value:
        cli_args.environments.prompt()


def generate_command_from_title(title: str) -> str:
    if not title:
        return "mt"

    words = title.split()
    if words[-1].lower() == "cli":
        words = words[:-1]

    if not words:
        return "mt"

    first_letters = [word[0].lower() for word in words]
    command = "".join(first_letters)

    command = remove_non_alphanumeric_chars(command)

    return command


def remove_non_alphanumeric_chars(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "", text)


def create_environments_from_input(environment_names: List[str]) -> List[Env]:
    environments = []
    for env_name in environment_names:
        alias = generate_alias_from_name(env_name)
        environments.append(Env(name=env_name.strip(), alias=alias.lower()))
    return environments


def generate_alias_from_name(name: str) -> str:
    words = name.split("-")
    return "".join([word[0] for word in words])


def create_config_file(cli_args: Args, environments: List[Env]) -> str:
    config = ConfigFile(
        cli=Cli(name=cli_args.title.value, command=cli_args.command.value),
        envs=environments,
        tools=[],
    )

    dir_path = Path(cli_args.dir_name.value).resolve()
    app_yml_path = os.path.join(dir_path, "app.yml")
    write_file(
        app_yml_path,
        config.model_dump(mode="json", exclude_none=True, exclude_unset=True),
    )

    return app_yml_path


def display_success_message(cli_args: Args, config_path: str) -> None:
    log.info(
        _("msg.actions.internal.create_cli.success"),
        gap_end=1,
        gap_start=1,
    )
    log.result(f"[b]CLI project created at: {Path(cli_args.dir_name.value).resolve()}")
    log.info(
        _("msg.actions.internal.create_cli.install_instructions").format(
            command=cli_args.command.value
        ),
        gap_start=1,
    )
    log.result(f"[b]$ hexagon install {config_path}")

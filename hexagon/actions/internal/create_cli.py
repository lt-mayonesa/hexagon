import os
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
        prompt_message=_("action.actions.internal.create_cli.directory_name"),
    )
    title: OptionalArg[str] = Arg(
        None,
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
    # Ask for directory name if not provided
    if not cli_args.dir_name.value:
        cli_args.dir_name.prompt()

    # Create directory
    dir_path = Path(cli_args.dir_name.value).resolve()
    if dir_path.exists() and any(Path(dir_path).iterdir()):
        if not prompt.confirm(
            _("action.actions.internal.create_cli.directory_not_empty").format(
                dir_name=dir_path
            )
        ):
            log.info(_("msg.actions.internal.create_cli.directory_not_empty_cancelled"))
            return
    os.makedirs(dir_path, exist_ok=True)

    # Prompt for CLI title if not provided
    if not cli_args.title.value:
        cli_args.title.prompt()

    # Prompt for command if not provided
    if not cli_args.command.value:
        cli_args.command.prompt(
            default=cli_args.dir_name.value.lower().replace(" ", "-")
        )

    # Prompt for environments if not provided
    if not cli_args.environments.value:
        cli_args.environments.prompt()

    # Parse environments and create aliases
    envs = []
    for env in cli_args.environments.value:
        alias = _first_letter_of_each_word(env)

        envs.append(Env(name=env.strip(), alias=alias.lower()))

    # Create app.yml content
    config = ConfigFile(
        cli=Cli(name=cli_args.title.value, command=cli_args.command.value),
        envs=envs,
        tools=[],
    )

    # Write app.yml file
    app_yml_path = os.path.join(dir_path, "app.yml")
    write_file(
        app_yml_path,
        config.model_dump(mode="json", exclude_none=True, exclude_unset=True),
    )

    # Print success message
    log.info(
        _("msg.actions.internal.create_cli.success"),
        gap_end=1,
        gap_start=1,
    )
    log.result(f"[b]CLI project created at: {dir_path}")
    log.info(
        _("msg.actions.internal.create_cli.install_instructions").format(
            command=cli_args.command.value
        ),
        gap_start=1,
    )
    log.result(f"[b]$ hexagon install {app_yml_path}")


def _first_letter_of_each_word(env):
    words = env.split("-")
    alias = "".join([word[0] for word in words])
    return alias

import os

from hexagon.runtime.options import CLI_OPTIONS_FILE_NAME, Options
from hexagon.runtime.singletons import configuration
from hexagon.support.config_file import ConfigFileManager
from hexagon.support.input.args import ToolArgs, PositionalArg, Arg, OptionalArg
from hexagon.support.output.printer import log

_OPTION_FIELD_NAMES = [f for f in Options.model_fields if not f.startswith("_")]


class Args(ToolArgs):
    action: PositionalArg[str] = Arg(
        None,
        prompt_message=_("action.actions.internal.manage_cli_options.choose_action"),
    )
    key: OptionalArg[str] = Arg(
        None,
        prompt_message=_("action.actions.internal.manage_cli_options.input_key"),
    )
    value: OptionalArg[str] = Arg(
        None,
        prompt_message=_("action.actions.internal.manage_cli_options.input_value"),
    )


def _options_file_path() -> str:
    return os.path.join(configuration.project_path or ".", CLI_OPTIONS_FILE_NAME)


def main(tool, env, env_args, cli_args):
    action = cli_args.action.prompt(
        searchable=True,
        choices=["list", "set", "unset"],
        validate=lambda x: x,
    )

    manager = ConfigFileManager(_options_file_path())

    if action == "list":
        _list_options(manager)
    elif action == "set":
        _set_option(manager, cli_args)
    elif action == "unset":
        _unset_option(manager, cli_args)


def _list_options(manager: ConfigFileManager):
    data = manager.load()
    if not data:
        log.info(_("msg.actions.internal.manage_cli_options.no_options_file"))
        return

    log.info(
        _("msg.actions.internal.manage_cli_options.listing_options").format(
            path=manager.path
        )
    )
    for key, value in data.items():
        log.result(f"  {key}: {value}")


def _set_option(manager: ConfigFileManager, cli_args):
    key = cli_args.key.prompt(
        searchable=True,
        choices=_OPTION_FIELD_NAMES,
        validate=lambda x: x,
    )
    value = cli_args.value.prompt(
        message=_("action.actions.internal.manage_cli_options.input_value"),
        validate=lambda x: x,
    )

    if not manager.exists:
        manager.create()
        log.info(
            _("msg.actions.internal.manage_cli_options.file_created").format(
                path=manager.path
            )
        )

    manager.load()
    manager.set_value(key, value)
    manager.save()
    log.result(
        _("msg.actions.internal.manage_cli_options.option_set").format(
            key=key, value=value
        )
    )


def _unset_option(manager: ConfigFileManager, cli_args):
    if not manager.exists:
        log.info(_("msg.actions.internal.manage_cli_options.no_options_file"))
        return

    existing_keys = list(manager.load().keys())
    if not existing_keys:
        log.info(_("msg.actions.internal.manage_cli_options.no_options_set"))
        return

    key = cli_args.key.prompt(
        searchable=True,
        choices=existing_keys,
        validate=lambda x: x,
    )

    removed = manager.unset_value(key)
    if removed:
        manager.save()
        log.result(
            _("msg.actions.internal.manage_cli_options.option_unset").format(key=key)
        )
    else:
        log.info(
            _("msg.actions.internal.manage_cli_options.option_not_found").format(
                key=key
            )
        )

import os
from shutil import copytree

from pydantic import DirectoryPath

from hexagon.actions import external
from hexagon.domain.tool import ActionTool, ToolType
from hexagon.runtime.singletons import configuration
from hexagon.support.input.args import ToolArgs, PositionalArg, Arg, OptionalArg
from hexagon.support.output.printer import log


class Args(ToolArgs):
    action: PositionalArg[str] = Arg(
        None, prompt_message=_("action.actions.internal.create_new_tool.choose_action")
    )
    type: OptionalArg[ToolType] = Arg(
        None, prompt_message=_("action.actions.internal.create_new_tool.choose_type")
    )
    name: OptionalArg[str] = Arg(
        None, prompt_message=_("action.actions.internal.create_new_tool.input_name")
    )
    alias: OptionalArg[str] = Arg(
        None, prompt_message=_("action.actions.internal.create_new_tool.input_alias")
    )
    long_name: OptionalArg[str] = Arg(
        None,
        prompt_message=_("action.actions.internal.create_new_tool.input_long_name"),
    )
    description: OptionalArg[str] = Arg(
        None,
        prompt_message=_("action.actions.internal.create_new_tool.input_description"),
    )
    custom_tools_path: OptionalArg[DirectoryPath] = Arg(
        ".",
        prompt_message=_(
            "action.actions.internal.create_new_tool.input_custom_tools_path"
        ),
    )


def main(tool, env, env_args, cli_args):
    create_action = False
    new_tool = ActionTool(
        name="invalid",
        action=cli_args.action.prompt(
            searchable=True,
            choices=external.__all__ + ["new_action"],
            validate=lambda x: x,
        ),
    )

    if new_tool.action == "new_action":
        create_action = True
        new_tool.action = cli_args.action.prompt(
            message=_("action.actions.internal.create_new_tool.input_action"),
            validate=lambda x: x,
        )

    new_tool.type = cli_args.type.prompt(
        choices=[
            {"value": ToolType.web, "name": ToolType.web.value},
            {"value": ToolType.shell, "name": ToolType.shell.value},
        ],
        default=ToolType.web if new_tool.action == "open_link" else ToolType.shell,
    )

    new_tool.name = cli_args.name.prompt(
        validate=lambda x: x,
        default=new_tool.action.replace("_", "-"),
    )

    new_tool.alias = cli_args.alias.prompt(
        default="".join([z[:1] for z in new_tool.name.split("-")]),
        filter=lambda r: r or None,
    )

    new_tool.long_name = cli_args.long_name.prompt(filter=lambda r: r or None)

    new_tool.description = cli_args.description.prompt(filter=lambda r: r or None)

    cli, tools, envs = configuration.refresh()

    if create_action:
        if not configuration.custom_tools_path:
            log.info(_("msg.actions.internal.create_new_tool.custom_tools_dir_not_set"))
            path_ = cli_args.custom_tools_path.prompt()
            configuration.update_custom_tools_path(
                (
                    path_.resolve()
                    if path_.is_absolute()
                    else os.path.join(*path_.parents, path_.name)
                ),
                comment=_(
                    "msg.actions.internal.create_new_tool.input_custom_tools_path_comment"
                ),
            )

        copytree(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "..",
                    "actions",
                    "__templates",
                    "custom_tool",
                )
            ),
            os.path.join(configuration.custom_tools_path, new_tool.action),
        )

        _replace_variables(
            os.path.join(configuration.custom_tools_path, new_tool.action, "README.md"),
            "{{tool}}",
            new_tool.long_name or new_tool.name,
        )

    configuration.add_tool(new_tool)
    configuration.save()


def _replace_variables(file_name, variable, value):
    with open(file_name, "r") as file:
        file_data = file.read()

    file_data = file_data.replace(variable, value)

    with open(file_name, "w") as file:
        file.write(file_data)

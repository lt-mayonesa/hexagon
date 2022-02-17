import os
from shutil import copytree

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from hexagon.actions import external
from hexagon.domain import configuration
from hexagon.domain.tool import ActionTool, ToolType
from hexagon.support.printer import log


def main(*__):
    create_action = False
    new_tool = ActionTool(
        name="invalid",
        action=inquirer.fuzzy(
            message=_("action.actions.internal.create_new_tool.choose_action"),
            validate=lambda x: x,
            choices=external.__all__ + ["new_action"],
        ).execute(),
    )

    if new_tool.action == "new_action":
        create_action = True
        new_tool.action = inquirer.text(
            message=_("action.actions.internal.create_new_tool.input_action"),
            validate=lambda x: x,
        ).execute()

    new_tool.type = inquirer.select(
        message=_("action.actions.internal.create_new_tool.choose_type"),
        choices=[
            {"value": ToolType.web, "name": ToolType.web.value},
            {"value": ToolType.shell, "name": ToolType.shell.value},
        ],
        default=ToolType.web if new_tool.action == "open_link" else ToolType.shell,
    ).execute()

    new_tool.name = inquirer.text(
        message=_("action.actions.internal.create_new_tool.input_name"),
        validate=lambda x: x,
        default=new_tool.action.replace("_", "-"),
    ).execute()

    new_tool.alias = inquirer.text(
        message=_("action.actions.internal.create_new_tool.input_alias"),
        default="".join([z[:1] for z in new_tool.name.split("-")]),
        filter=lambda r: r or None,
    ).execute()

    new_tool.long_name = inquirer.text(
        message=_("action.actions.internal.create_new_tool.input_long_name"),
        filter=lambda r: r or None,
    ).execute()

    new_tool.description = inquirer.text(
        message=_("action.actions.internal.create_new_tool.input_description"),
        filter=lambda r: r or None,
    ).execute()

    cli, tools, envs = configuration.refresh()

    if create_action:
        if not configuration.custom_tools_path:
            log.info(_("msg.actions.internal.create_new_tool.custom_tools_dir_not_set"))
            configuration.update_custom_tools_path(
                inquirer.filepath(
                    message=_(
                        "action.actions.internal.create_new_tool.input_custom_tools_path"
                    ),
                    default=".",
                    validate=PathValidator(
                        is_dir=True,
                        message=_(
                            "error.actions.internal.create_new_tool.insert_valid_directory"
                        ),
                    ),
                ).execute(),
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
                    "support",
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

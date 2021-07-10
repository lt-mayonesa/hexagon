import os
from shutil import copytree

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from hexagon.domain.tool import Tool, ToolType
from hexagon.domain import configuration
from hexagon.tools import external
from hexagon.support.printer import log


def main(*_):
    create_action = False
    new_tool = Tool(
        action=inquirer.fuzzy(
            message="Choose the action of your tool:",
            validate=lambda x: x,
            choices=external.__all__ + ["new_action"],
        ).execute()
    )

    if new_tool.action == "new_action":
        create_action = True
        new_tool.action = inquirer.text(
            message="What name would you like to give your new action?",
            validate=lambda x: x,
        ).execute()

    new_tool.type = inquirer.select(
        message="What type of tool is it?",
        choices=[
            {"value": ToolType.web, "name": ToolType.web.value},
            {"value": ToolType.shell, "name": ToolType.shell.value},
        ],
        default=ToolType.web if new_tool.action == "open_link" else ToolType.shell,
    ).execute()

    command = inquirer.text(
        message="What command would you like to give your tool?",
        validate=lambda x: x,
        default=new_tool.action.replace("_", "-"),
    ).execute()

    new_tool.alias = inquirer.text(
        message="Would you like to add an alias/shortcut? (empty for none)",
        default="".join([z[:1] for z in command.split("-")]),
        filter=lambda r: r or None,
    ).execute()

    new_tool.long_name = inquirer.text(
        message="Would you like to add a long name? (this will be displayed instead of command)",
        filter=lambda r: r or None,
    ).execute()

    new_tool.description = inquirer.text(
        message="Would you like to add a description? (this will be displayed along side command/long_name)",
        filter=lambda r: r or None,
    ).execute()

    cli, tools, _ = configuration.refresh()

    if create_action:
        if not configuration.custom_tools_path:
            log.info("[magenta]Your CLI does not have a custom tools dir.")
            configuration.update_custom_tools_path(
                inquirer.filepath(
                    message="Where would you like it to be? "
                    "(can be absolute path or relative to YAML. ie: ./tools or .)",
                    default=".",
                    validate=PathValidator(
                        is_dir=True, message="Please select a valid directory"
                    ),
                ).execute(),
                comment="relative to this file",
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
            new_tool.long_name or command,
        )

    configuration.add_tool(command, new_tool)
    configuration.save()


def _replace_variables(file_name, variable, value):
    with open(file_name, "r") as file:
        file_data = file.read()

    file_data = file_data.replace(variable, value)

    with open(file_name, "w") as file:
        file.write(file_data)

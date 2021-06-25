import os
from shutil import copytree

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from rich import print

from hexagon.cli.config import configuration
from hexagon.tools import external


def main(_):
    create_action = False
    output = {
        'action': inquirer.fuzzy(
            message='Choose the action of your tool:',
            validate=lambda x: x,
            choices=external.__all__ + ['new_action']
        ).execute()
    }

    if output['action'] == 'new_action':
        create_action = True
        output['action'] = inquirer.text(
            message='What name would you like to give your new action?',
            validate=lambda x: x
        ).execute()

    output['type'] = inquirer.select(
        message='What type of tool is it?',
        choices=['web', 'shell'],
        default='web' if output['action'] == 'open_link' else 'shell'
    ).execute()

    command = inquirer.text(
        message='What command would you like to give your tool?',
        validate=lambda x: x,
        default=output['action'].replace('_', '-')
    ).execute()

    output['alias'] = inquirer.text(
        message='Would you like to add an alias/shortcut? (empty for none)',
        default=''.join([z[:1] for z in command.split('-')])
    ).execute()

    output['long_name'] = inquirer.text(
        message='Would you like to add a long name? (this will be displayed instead of command)'
    ).execute()

    output['description'] = inquirer.text(
        message='Would you like to add a description? (this will be displayed along side command/long_name)'
    ).execute()

    cli, tools, _ = configuration.refresh()

    if create_action:
        if not configuration.custom_tools_path:
            print('│ [magenta]Your CLI does not have a custom tools dir.')
            configuration.update_custom_tools_path(
                inquirer.filepath(
                    message='Where would you like it to be? '
                            '(can be absolute path or relative to YAML. ie: ./tools or .)',
                    default='.',
                    validate=PathValidator(is_dir=True, message='Please select a valid directory')
                ).execute(),
                comment='relative to this file')

        copytree(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'cli', '__templates', 'custom_tool')),
            os.path.join(configuration.custom_tools_path, output['action']))

        _replace_variables(os.path.join(configuration.custom_tools_path, output['action'], 'README.md'), '{{tool}}',
                           output.get('long_name', command))

    configuration.add_tool(command, {k: v for k, v in output.items() if v != ''})

    configuration.save()


def _replace_variables(file_name, variable, value):
    with open(file_name, 'r') as file:
        file_data = file.read()

    file_data = file_data.replace(variable, value)

    with open(file_name, 'w') as file:
        file.write(file_data)

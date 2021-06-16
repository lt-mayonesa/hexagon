import os
from shutil import copytree

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from ruamel.yaml import YAML

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

    yaml = YAML()

    # TODO: esto no es DRY, se viene un refactor
    with open(os.environ['HEXAGON_CONFIG_FILE'], 'r+') as f:
        config_file = yaml.load(f)
        f.seek(0)

        if create_action:
            if 'custom_tools_dir' not in config_file['cli']:
                src_path = inquirer.filepath(
                    message="Your CLI does not have a custom tools dir."
                            "Where would you like it to be? (can be absolute path or relative to YAML)",
                    default='.',
                    validate=PathValidator(is_dir=True, message="Please select a valid directory")
                ).execute()
                config_file['cli'].insert(0, 'custom_tools_dir', src_path, 'relative to this file')
            else:
                src_path = config_file['cli']['custom_tools_dir']

            copytree(f'{os.path.dirname(__file__)}/../../cli/__templates/custom_tool', f"{src_path}/{command}")
            _replace_variables(f"{src_path}/{command}/README.md", '{{tool}}',
                               output['long_name'] if 'long_name' in output else command)

        _add_tool(command, config_file, output)

        yaml.dump(config_file, f)


def _add_tool(command, config_file, output):
    config_file['tools'].insert(
        len(config_file['tools']), command, {k: v for k, v in output.items() if v != ''})
    config_file['tools'].yaml_set_comment_before_after_key(command, before='\n')


def _replace_variables(file_name, variable, value):
    with open(file_name, 'r') as file:
        file_data = file.read()

    file_data = file_data.replace(variable, value)

    with open(file_name, 'w') as file:
        file.write(file_data)

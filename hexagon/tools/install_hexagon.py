from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from prompt_toolkit.validation import ValidationError

from hexagon.cli.config import init_config
from hexagon.tools.save_new_alias import save_new_alias


class YamlFileValidator(PathValidator):

    def validate(self, document) -> None:
        super(YamlFileValidator, self).validate(document)
        extension = document.text.split('/')[-1].split('.')[-1]
        if extension != 'yaml' and extension != 'yml':
            raise ValidationError(
                message=self.message,
                cursor_position=document.cursor_position,
            )


def install_hexagon(_):
    src_path = inquirer.filepath(
        message="Where is your project's hexagon config file?",
        default=str(Path.cwd()),
        validate=YamlFileValidator(is_file=True, message="Please select a valid YAML file")
    ).execute()

    cli_config, tools, envs = init_config(src_path)

    save_new_alias(None, name=cli_config['command'], command=f'HEXAGON_CONFIG_FILE={src_path} hexagon')

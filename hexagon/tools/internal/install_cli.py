from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from prompt_toolkit.validation import ValidationError
from ruamel.yaml import YAML

from hexagon.tools.internal.save_new_alias import save_new_alias


class YamlFileValidator(PathValidator):

    def validate(self, document) -> None:
        super(YamlFileValidator, self).validate(document)
        extension = document.text.split('/')[-1].split('.')[-1]
        if extension != 'yaml' and extension != 'yml':
            raise ValidationError(
                message=self.message,
                cursor_position=document.cursor_position,
            )


def main(_):
    src_path = inquirer.filepath(
        message="Where is your project's hexagon config file?",
        default=str(Path.cwd()),
        validate=YamlFileValidator(is_file=True, message="Please select a valid YAML file")
    ).execute()

    with open(src_path, 'r') as f:
      command = YAML().load(f)['cli']['command']    

    save_new_alias(command, f'HEXAGON_CONFIG_FILE={src_path} hexagon')

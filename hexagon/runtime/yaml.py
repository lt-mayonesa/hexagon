import os
from typing import Any, Type

from pydantic import ValidationError
from ruamel import yaml
from ruamel.yaml import YAML

from hexagon.domain.hexagon_error import HexagonError
from hexagon.support.output.printer import Logger


def read_file(path: str) -> Any:
    try:
        return YAML().load(open(path, "r"))
    except FileNotFoundError:
        return None


def write_file(path: str, content: str):
    with open(path, "w") as f:
        YAML().dump(content, f)
    return True


def load_model(model: Type, content: dict, path: str):
    try:
        return model(**content)
    except ValidationError as error:
        raise YamlValidationError(error, content, path)


class YamlValidationError(HexagonError):
    def __init__(self, error: ValidationError, yaml_content=None, yaml_path=None):
        self.yaml_content = yaml_content
        self.yaml_path = yaml_path
        self.errors = error.errors()
        self.actual_yaml_file = open(yaml_path, "r").read() if yaml_path else None
        super().__init__(self._error_printer)

    def _error_printer(self, logger: Logger):
        logger.error(
            _("error.support.yaml.invalid_yaml").format(
                errors_length=len(self.errors), yaml_path=self.yaml_path
            )
        )
        for err in self.errors:
            logger.error(
                os.linesep  # this \n can not go in the .po file because it breaks msgmt
                + _("error.support.yaml.error_at").format(
                    loc=".".join(map(lambda i: str(i), err["loc"])), message=err["msg"]
                )
            )
            if self.yaml_content and yaml:
                (start, line_number, end) = self.__lines_of_error(
                    err, self.yaml_content
                )
                logger.example(
                    "\n".join(self.actual_yaml_file.splitlines()[start:end]),
                    syntax="yaml",
                    show_line_numbers=True,
                    start_line=start + 1,
                    decorator_start=False,
                    decorator_end=False,
                )

    @classmethod
    def __lines_of_error(cls, err, ruamel_yaml):
        line_number = cls.__yaml_line_number(ruamel_yaml, err["loc"])
        return (
            max(0, line_number - 3),
            line_number,
            line_number + 2 if line_number != 0 else line_number,
        )

    @classmethod
    def __yaml_line_number(cls, yml, loc: list, line_count_hack: int = 0):
        """
        Get line number of location by accessing YAML metadata

        :param yml: a dict representing de YAML, usually created with YAML().load(file)
        :param loc: a list of the keys in the YAML
        :param line_count_hack: a counter to indicate nested level,
        for some reason ruamel .lc returns one less line_number for each level
        :return: the line number of loc
        """
        if len(loc) == 1:
            try:
                return (
                    line_count_hack + yml[loc[0]].lc.line
                    if yml[loc[0]]
                    else yml.lc.data[loc[0]][2]
                )
            except (LookupError, TypeError, AttributeError):
                return (
                    line_count_hack - 1 if line_count_hack > 0 else line_count_hack
                ) + yml.lc.line
        else:
            return cls.__yaml_line_number(
                yml[loc[0]], loc[1:], line_count_hack=line_count_hack + 1
            )

from pydantic import ValidationError
from rich.syntax import Syntax
from ruamel import yaml

from hexagon.support.printer import log


def display_yaml_errors(errors: ValidationError, ruamel_yaml=None, yaml_path=None):
    yml = open(yaml_path, "r").read() if yaml_path else None
    errors_as_dict = errors.errors()
    log.error(
        # There were {errors_length} error(s) in your YAML file: {yaml_path}
        _("error.support.yaml.invalid_yaml").format(
            errors_length=len(errors_as_dict), yaml_path=yaml_path
        )
    )
    for err in errors_as_dict:
        log.error(
            f"\n✗ [u][bold]{'.'.join(map(lambda i: str(i), err['loc']))}[/bold] -> {err['msg']}"
        )
        if ruamel_yaml and yaml:
            (start, line_number, end) = __lines_of_error(err, ruamel_yaml)
            log.example(
                Syntax(
                    "\n".join(yml.splitlines()[start:end]),
                    "yaml",
                    line_numbers=True,
                    start_line=start + 1,
                ),
                decorator_start=False,
                decorator_end=False,
            )


def __lines_of_error(err, ruamel_yaml):
    line_number = __yaml_line_number(ruamel_yaml, err["loc"])
    return (
        max(0, line_number - 3),
        line_number,
        line_number + 2 if line_number != 0 else line_number,
    )


def __yaml_line_number(yml, loc: list, line_count_hack: int = 0):
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
        return __yaml_line_number(
            yml[loc[0]], loc[1:], line_count_hack=line_count_hack + 1
        )

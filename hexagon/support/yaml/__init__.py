from pydantic import ValidationError
from rich.syntax import Syntax

from hexagon.support.printer import log


def display_yaml_errors(errors: ValidationError, ruamel_yaml, yaml_path):
    yml = open(yaml_path, "r").read()
    errors_as_dict = errors.errors()
    log.error(f"There were {len(errors_as_dict)} error(s) in your YAML")
    for err in errors_as_dict:
        (start, line_number, end) = __lines_of_error(err, ruamel_yaml)
        log.error(
            f"\n✗ [u][bold]{'.'.join(map(lambda i: str(i), err['loc']))}[/bold] -> {err['msg']}"
        )
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
            return line_count_hack + yml[loc[0]].lc.line
        except (LookupError, TypeError):
            return (
                line_count_hack - 1 if line_count_hack > 0 else line_count_hack
            ) + yml.lc.line
    else:
        return __yaml_line_number(
            yml[loc[0]], loc[1:], line_count_hack=line_count_hack + 1
        )

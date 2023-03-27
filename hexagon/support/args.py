import argparse
import re
import sys
from typing import Optional, Dict, List, Union

from pydantic import BaseModel

ARGUMENT_KEY_PREFIX = "--"


def cli_arg(cli_arguments, index):
    return (
        cli_arguments[index] if cli_arguments and len(cli_arguments) > index else None
    )


class CliArgs(BaseModel):
    show_help: bool = False
    tool: Optional[str] = None
    env: Optional[str] = None

    extra_args: Optional[Dict[str, Union[list, bool, int, str]]] = None
    raw_extra_args: Optional[List[str]] = None

    def as_list(self):
        return [self.tool, self.env] + (
            self.raw_extra_args if self.raw_extra_args else []
        )

    @staticmethod
    def key_value_arg(key, arg):
        return f"{ARGUMENT_KEY_PREFIX}{key}={arg}"


def parse_cli_args(args=None):
    if args is None:
        args = sys.argv[1:]

    _parser = __init_parser()

    known_args, extra = _parser.parse_known_args(args)

    if (not known_args.tool and not known_args.env) and any(
        [a in ["-h", "--help"] for a in args]
    ):
        return CliArgs(show_help=True)

    extra_args = __guess_optional_keys(extra)
    data = vars(known_args)
    data.update(
        {
            "raw_extra_args": extra,
            "extra_args": extra_args if extra_args else None,
        }
    )
    return CliArgs(**data)


def __init_parser():
    """
    Add Pydantic model to an ArgumentParser
    """
    __p = argparse.ArgumentParser(
        prog="hexagon", description="Hexagon CLI", add_help=False
    )
    __add_parser_argument(__p, CliArgs.__fields__.get("tool"))
    __add_parser_argument(__p, CliArgs.__fields__.get("env"))
    return __p


def __add_parser_argument(parser, field):
    parser.add_argument(
        field.name,
        nargs="?",
        type=__validate_special_characters(field.name),
        default=field.default,
        help=field.field_info.description,
    )


def __validate_special_characters(field_name):
    def field(value):
        if value and not re.match("^[a-zA-Z0-9\\-_]+$", value):
            raise ValueError(
                f"{field_name} must be a string and not contain special characters"
            )
        return value

    return field


def __guess_optional_keys(extra: List[str]):
    """
    Return a dict by guessing optional keys from a list of arguments, e.g.:
    ['--number', '123', '--name', 'John', '--name', 'Doe'] -> {'number': '123','name': ['John', 'Doe']}
    ['123'] -> {'0': '123'}
    ['123', '--letter', 'A'] -> {'0': '123', 'letter': 'A'}
    :param extra:
    :return:
    """
    if not extra:
        return None

    result = __args_to_key_vals(extra)
    return __group_by_key_appending(result)


def __args_to_key_vals(extra):
    result = []
    i = 0
    arg_index = 0
    while i < len(extra):
        if extra[i].startswith(ARGUMENT_KEY_PREFIX):
            if "=" in extra[i]:
                key, value = extra[i][2:].split("=")
                result.append({key: value})
                i += 1
            elif extra[i + 1].startswith(ARGUMENT_KEY_PREFIX):
                result.append({extra[i][2:]: True})
                i += 1
            else:
                result.append({extra[i][2:]: extra[i + 1]})
                i += 2
        else:
            result.append({str(arg_index): extra[i]})
            i += 1
            arg_index += 1
    return result


def __group_by_key_appending(result):
    d = {}
    for r in result:
        for k, v in r.items():
            if k in d:
                if isinstance(d[k], list):
                    d[k].append(v)
                else:
                    d[k] = [d[k], v]
            else:
                d[k] = v
    return d

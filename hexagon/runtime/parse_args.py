import argparse
import sys
from typing import List, get_origin

from pydantic import TypeAdapter
from pydantic_core import PydanticUndefined

from hexagon.support.input.args import (
    CliArgs,
    ARGUMENT_KEY_PREFIX,
    OptionalArg,
    PositionalArg,
)
from hexagon.support.input.args.field_reference import FieldReference
from hexagon.typing import should_support_multiple_args, field_type_information


# noinspection PyProtectedMember
class HexagonFormatter(argparse.RawDescriptionHelpFormatter):
    pass


def cli_arg(cli_arguments, index):
    return (
        cli_arguments[index] if cli_arguments and len(cli_arguments) > index else None
    )


def parse_cli_args(args=None, model=CliArgs, **kwargs):
    if args is None:
        args = sys.argv[1:]

    _parser = init_arg_parser(model, **kwargs)

    known_args, extra = _parser.parse_known_args(args)

    if __no_known_args(known_args) and __arg_any_of(args, ["-h", "--help"]):
        return model(show_help=True, total_args=0)

    if __no_known_args(known_args) and __arg_any_of(extra, ["-v", "--version"]):
        return model(show_version=True, total_args=0)

    if model == CliArgs:
        known_args, extra = __fix_misattributed_env_value(known_args, args, extra)

    count, extra_args = __guess_optional_keys(extra)
    data = vars(known_args)
    data.update(
        {
            "raw_extra_args": extra,
            "extra_args": extra_args if extra_args else None,
            "total_args": len(list(x for x in known_args.__dict__.values() if x))
            + count,
        }
    )
    return model(**{k: v for k, v in data.items() if v is not None})


def __arg_any_of(args, values):
    return any([a in values for a in args])


def __no_known_args(known_args):
    return all(not x for x in known_args.__dict__.values())


def __fix_misattributed_env_value(known_args, args, extra):
    """
    Fixes argparse incorrectly assigning values to 'env' that belong to unknown options.

    When parsing ['tool', '--unknown', 'value'], argparse may consume 'value' as env
    instead of leaving it for the unknown option. This function detects and corrects
    that by checking if env's value immediately follows an unknown flag in the args.
    """
    if not (hasattr(known_args, "env") and known_args.env and extra):
        return known_args, extra

    if not any(e.startswith(ARGUMENT_KEY_PREFIX) for e in extra):
        return known_args, extra

    env_value = known_args.env
    try:
        env_index = args.index(env_value)
        if env_index > 0:
            preceding_arg = args[env_index - 1]
            if preceding_arg.startswith(ARGUMENT_KEY_PREFIX) and preceding_arg in extra:
                extra = extra + [env_value]
                known_args.env = None
    except ValueError:
        pass

    return known_args, extra


def init_arg_parser(
    model, fields=None, prog=None, description=None, add_help=False, epilog=None
):
    __p = argparse.ArgumentParser(
        prog=prog or "hexagon",
        description=description or "Hexagon CLI",
        add_help=add_help,
        epilog=epilog,
        formatter_class=HexagonFormatter,
    )

    for name, field in model.model_fields.items():
        if fields and name not in fields:
            continue
        if get_origin(field.annotation) in [PositionalArg, OptionalArg]:
            __add_parser_argument(__p, FieldReference(name, field))
    return __p


def __add_parser_argument(parser, field: FieldReference):
    reprs = field.info.annotation.cli_repr(field)
    nargs, action, constant_default, is_bool = __config_base_on_type(field.info)

    default = None if field.info.default is PydanticUndefined else field.info.default
    parser.add_argument(
        *[r for r in reprs if r],
        nargs=nargs,
        action=action,
        const=constant_default,
        help=f"{field.info.description or field.name} (default: {default})",
    )
    if is_bool:
        parser.add_argument(
            *[__bool_negated_key(r.replace("-", "")) for r in reprs if r],
            action="store_const",
            dest=field.name,
            const="false",
            help=f"Disable {field.name}",
        )


def __config_base_on_type(field):
    """
    Determines argparse configuration based on field type.

    Returns: (nargs, action, const, is_bool)

    Configuration by field type:
    - OptionalArg + collection: nargs="*", action="extend"
    - OptionalArg + bool: nargs="?", action="store"
    - OptionalArg + scalar: nargs=None, action="store"
    - PositionalArg: nargs="?", action="store"
    """
    field_type, _, __ = field_type_information(field)
    constant_default = "true" if field_type.is_bool else None
    is_optional_arg = get_origin(field.annotation) == OptionalArg
    is_collection = should_support_multiple_args(field)

    if is_optional_arg and is_collection:
        return "*", "extend", constant_default, field_type.is_bool
    elif is_optional_arg and field_type.is_bool:
        return "?", "store", constant_default, field_type.is_bool
    elif is_optional_arg:
        return None, "store", constant_default, field_type.is_bool
    else:
        return "?", "store", constant_default, field_type.is_bool


def __guess_optional_keys(extra: List[str]):
    """
    Return a dict by guessing optional keys from a list of arguments, e.g.:
    ['--number', '123', '--name', 'John', '--name', 'Doe'] -> {'number': 123,'name': ['John', 'Doe']}
    ['123'] -> {'0': 123}
    ['123', '--letter', 'A'] -> {'0': 123, 'letter': 'A'}
    :param extra:
    :return:
    """
    if not extra:
        return 0, None

    result = __args_to_key_vals(extra)
    return len(result), __group_by_key_appending(result)


def __args_to_key_vals(extra):
    result = []
    i = 0
    arg_index = 0
    while i < len(extra):
        current, next_ = extra[i], extra[i + 1] if i + 1 < len(extra) else None
        if current.startswith(ARGUMENT_KEY_PREFIX):
            if "=" in current:
                key, value = current[2:].split("=", 1)
                result.append({key: __adapt_value_type(value)})
                i += 1
            elif not next_ or next_.startswith(ARGUMENT_KEY_PREFIX):
                result.append({current[2:]: True})
                i += 1
            else:
                result.append({current[2:]: __adapt_value_type(next_)})
                i += 2
        else:
            result.append({str(arg_index): __adapt_value_type(current)})
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


def __bool_negated_key(name: str):
    return f"{ARGUMENT_KEY_PREFIX * 2}no-{name}"


def __adapt_value_type(value: str):
    result = __try_to_parse_type(value, bool)
    if result is not None:
        return result
    return __try_to_parse_type(value, int) or __try_to_parse_type(value, float) or value


def __try_to_parse_type(value: str, target: type):
    adapter = TypeAdapter(target)
    try:
        return adapter.validate_strings(value)
    except ValueError:
        return None

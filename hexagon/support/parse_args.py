import argparse
import sys
from typing import List

from pydantic.fields import ModelField

from hexagon.domain.args import CliArgs, ARGUMENT_KEY_PREFIX, OptionalArg, PositionalArg


def cli_arg(cli_arguments, index):
    return (
        cli_arguments[index] if cli_arguments and len(cli_arguments) > index else None
    )


def parse_cli_args(args=None):
    if args is None:
        args = sys.argv[1:]

    _parser = init_arg_parser(CliArgs)

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


def init_arg_parser(model, fields=None, prog=None, description=None):
    __p = argparse.ArgumentParser(
        prog=prog or "hexagon", description=description or "Hexagon CLI", add_help=False
    )

    if sys.version_info < (3, 8):
        __polyfill_extend_action(__p)

    for field in model.__fields__.values():
        if fields and field.name not in fields:
            continue
        if field.type_ in [PositionalArg, OptionalArg]:
            __add_parser_argument(__p, field)
    return __p


def __polyfill_extend_action(__p):
    class ExtendAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            items = getattr(namespace, self.dest) or []
            items.extend(values)
            setattr(namespace, self.dest, items)

    __p.register("action", "extend", ExtendAction)


def __add_parser_argument(parser, field: ModelField):
    reprs = field.type_.cli_repr(field)
    nargs, action = __config_base_on_type(field)
    parser.add_argument(
        *[x for x in reprs if x],
        nargs=nargs,
        action=action,
        default=field.default,
        help=field.field_info.description,
    )


def __config_base_on_type(field):
    """
    Return a tuple with the number of arguments and the action to be taken
    if the field is any kind of collection, nargs should be * and the action is "extend"
    :param field:
    :return:
    """
    return (
        (
            "*",
            "extend",
        )
        if field.type_ == OptionalArg and __should_support_multiple_args(field)
        else (
            "?",
            "store",
        )
    )


def __should_support_multiple_args(field):
    iterables = [list, tuple, set]
    t = field.outer_type_
    while hasattr(t, "__args__") and len(t.__args__) > 0:
        t = t.__args__[0]
        if hasattr(t, "__origin__") and t.__origin__ in iterables:
            return True

    return t in iterables


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
    # FIXME: handle case where optional arg is last, ie: "tool env --verbose"
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

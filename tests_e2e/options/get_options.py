from datetime import timedelta
from typing import Any, Dict

from hexagon.domain.singletons import options
from hexagon.support.printer import log


def _print_dict_indented(dictionary: Dict[str, Any], indent_level=0):
    for key, value in dictionary.items():
        if not value or isinstance(value, (str, int, float, timedelta)):
            log.result(" " * indent_level * 2 + f"{key}: {value}")
        else:
            log.result(key)
            _print_dict_indented(value.__dict__, indent_level + 1)


def main(*_):
    _print_dict_indented(options.__dict__)

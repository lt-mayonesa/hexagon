from enum import Enum
from typing import Any, Union, get_args, get_origin, Annotated

from pydantic.fields import FieldInfo

from hexagon.support.input.args import HexagonArg
from hexagon.support.input.args.errors import MultipleHintsNotSupportedError
from hexagon.typing.type_information import TypeInformation


def should_support_multiple_args(field: Union[FieldInfo, Any]):
    type_ = _field_type(field) if isinstance(field, FieldInfo) else field
    if hasattr(type_, "__origin__"):
        type_ = type_.__origin__
    return type_ in [list, tuple, set]


def field_type_information(field: FieldInfo):
    type_ = _field_type(field)
    iterable = should_support_multiple_args(field)
    if iterable and hasattr(type_, "__args__") and len(type_.__args__):
        of_enum = _is_enumerable(type_.__args__[0])
    else:
        of_enum = _is_enumerable(type_)

    return TypeInformation(type_), iterable, of_enum


def _field_type(field: FieldInfo):
    p = None
    t = field.annotation
    ars = get_args(t)
    while __needs_unpacking(t):
        p = t
        ars = get_args(t)
        t = ars[0]
    if get_origin(p) is Annotated:
        return p
    if len(ars) > 1 and ars[-1] is not type(None):
        raise MultipleHintsNotSupportedError(ars)
    return t


def __needs_unpacking(t):
    try:
        if (
            get_origin(t) is Union
            or issubclass(get_origin(t), HexagonArg)
            or get_origin(t) is Annotated
        ):
            return True
    except TypeError:
        return False


def _is_enumerable(type_):
    try:
        res = issubclass(type_, Enum)
    except TypeError:
        res = False
    return res

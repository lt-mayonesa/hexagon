from enum import Enum
from typing import Any, Union

from pydantic.fields import ModelField


def should_support_multiple_args(field: Union[ModelField, Any]):
    type_ = _field_type(field) if isinstance(field, ModelField) else field
    if hasattr(type_, "__origin__"):
        type_ = type_.__origin__
    return type_ in [list, tuple, set]


def field_info(field: ModelField):
    type_ = _field_type(field)
    iterable = should_support_multiple_args(field)
    if iterable and hasattr(type_, "__args__") and len(type_.__args__):
        of_enum = _is_enumerable(type_.__args__[0])
    else:
        of_enum = _is_enumerable(type_)

    return type_, iterable, of_enum


def _field_type(field: ModelField):
    return field.sub_fields[0].outer_type_


def _is_enumerable(type_):
    try:
        res = issubclass(type_, Enum)
    except TypeError:
        res = False
    return res

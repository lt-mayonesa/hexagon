import abc
from copy import copy
from typing import Generic, Union, Callable, TypeVar

from pydantic import ValidationError
from pydantic.fields import ModelField

ARGUMENT_KEY_PREFIX = "-"

T = TypeVar("T")


class HexagonArg(Generic[T]):
    __model__ = None
    __field__ = None

    def __init__(self, value: T):
        self.__value__ = value

    @classmethod
    def __get_validators__(cls):
        yield cls.arg_validator(cls)

    @property
    def value(self):
        if self.__model__:
            self.__model__.trace(self.__field__)
        return self.__value__

    def prompt(
        self,
        skip_trace: Union[bool, Callable] = False,
        **kwargs,
    ):
        """
        Prompt the user for a value for this argument.

        :param skip_trace: true if this prompt should not be traced by hexagon
        :param kwargs: any extra argument supported by hexagon and InquirePy
        :return:
        """
        if not self.__model__:
            raise ValueError(
                "Cannot prompt for a value when model reference is not initialized. "
                "Probably _init_refs was not called."
            )
        return self.__model__.prompt(self.__field__, skip_trace, **kwargs)

    def _init_refs(self, model, field):
        self.__field__ = field
        self.__model__ = model

    @staticmethod
    @abc.abstractmethod
    def cli_repr(field: ModelField):
        return

    def __str__(self, **kwargs):
        return str(self.__value__)

    @staticmethod
    def arg_validator(cls):
        def validate(v, field: ModelField):
            if not isinstance(v, cls):
                v = cls(v)
            if not field.sub_fields:
                # Generic parameters were not provided, ie: `name = PositionalArg`,
                # so we don't try to validate them and just return the value as is
                return v
            value = field.sub_fields[0]

            value.field_info.extra = copy(field.field_info.extra)
            valid_value, error = value.validate(v.__value__, {}, loc="")
            if error:
                raise ValidationError([error], model=cls)
            return cls(valid_value)

        return validate


class PositionalArg(HexagonArg[T]):
    @staticmethod
    def cli_repr(field: ModelField):
        return field.name, None


class OptionalArg(HexagonArg[T]):
    @staticmethod
    def cli_repr(field: ModelField):
        def initials_from(name: str):
            return "".join([w[0] for w in name.split("_")])

        return (
            name_key(field.name.replace("_", "-")),
            alias_key(
                field.alias.replace("_", "-")
                if field.alias and field.alias != field.name
                else initials_from(field.name)
            ),
        )


def name_key(name: str):
    return f"{ARGUMENT_KEY_PREFIX * 2}{name}"


def alias_key(alias: str):
    return f"{ARGUMENT_KEY_PREFIX}{alias}"

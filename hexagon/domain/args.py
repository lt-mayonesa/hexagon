import re
from typing import Optional, Dict, Union, List, TypeVar, Generic

from pydantic import BaseModel, validator, ValidationError
from pydantic.fields import ModelField

ARGUMENT_KEY_PREFIX = "-"


T = TypeVar("T")


def arg_validator(cls):
    def validate(v, field: ModelField):
        if not isinstance(v, cls):
            v = cls(v)
        if not field.sub_fields:
            # Generic parameters were not provided, ie: `name = PositionalArg`,
            # so we don't try to validate them and just return the value as is
            return v
        value = field.sub_fields[0]

        valid_value, error = value.validate(v.value, {}, loc="")
        if error:
            raise ValidationError([error], model=cls)
        return valid_value

    return validate


class PositionalArg(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    @classmethod
    def __get_validators__(cls):
        yield arg_validator(cls)

    @staticmethod
    def cli_repr(field: ModelField):
        return (
            field.name,
            field.alias if field.alias and field.alias != field.name else None,
        )


class OptionalArg(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    @classmethod
    def __get_validators__(cls):
        yield arg_validator(cls)

    @staticmethod
    def cli_repr(field: ModelField):
        return (
            f"{ARGUMENT_KEY_PREFIX*2}{field.name.replace('_', '-')}",
            f"{ARGUMENT_KEY_PREFIX}{field.alias.replace('_', '-')}"
            if field.alias and field.alias != field.name
            else f"{ARGUMENT_KEY_PREFIX}{''.join([w[0] for w in field.name.split('_')])}",
        )


class CliArgs(BaseModel):
    show_help: bool = False
    tool: PositionalArg[Optional[str]] = None
    env: PositionalArg[Optional[str]] = None

    extra_args: Optional[Dict[str, Union[list, bool, int, str]]] = None
    raw_extra_args: Optional[List[str]] = None

    def as_list(self):
        return [self.tool, self.env] + (
            self.raw_extra_args if self.raw_extra_args else []
        )

    @validator("tool", "env")
    def validate(cls, v, field):
        if v and not re.match("^[a-zA-Z0-9\\-_]+$", v):
            raise ValueError(
                f"{field.name} must be a string and not contain special characters"
            )
        return v

    @staticmethod
    def key_value_arg(key, arg):
        prefix = ARGUMENT_KEY_PREFIX * (2 if len(key) > 2 else 1)
        return f"{prefix}{key}={arg}"


class ToolArgs(BaseModel):
    __tracer__ = None
    show_help: bool = False
    extra_args: Optional[Dict[str, Union[list, bool, int, str]]] = None
    raw_extra_args: Optional[List[str]] = None

    def __getattribute__(self, item, skip_tracing=False):
        if item == "__fields__":
            return super().__getattribute__(item)
        if item in self.__fields__:
            if skip_tracing:
                return super().__getattribute__(item)

            if not self.__tracer__:
                raise Exception("Tracer not set")

            field = self.__fields__.get(item)
            value_ = self.__getattribute__(item, skip_tracing=True)
            if value_ != field.default:
                if field.type_ == PositionalArg:
                    self.__tracer__.tracing(value_)
                elif field.type_ == OptionalArg:
                    self.__tracer__.tracing(
                        value_,
                        key=item.replace("_", "-"),
                    )

        return super().__getattribute__(item)

    def with_tracer(self, tracer):
        self.__tracer__ = tracer
        return self

    class Config:
        underscore_attrs_are_private = True

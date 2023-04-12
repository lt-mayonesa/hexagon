import re
from typing import Optional, Dict, Union, List, TypeVar, Generic, Any

from pydantic import (
    BaseModel,
    validator as pydantic_validator,
    ValidationError,
    Field as PydanticField,
)
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
        return cls(valid_value)

    return validate


class PositionalArg(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    @classmethod
    def __get_validators__(cls):
        yield arg_validator(cls)

    @staticmethod
    def cli_repr(field: ModelField):
        return field.name, None

    def __str__(self, **kwargs):
        return str(self.value)


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

    def __str__(self, **kwargs):
        return str(self.value)


# noinspection PyPep8Naming
def Arg(
    default: Any = None,
    *,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    prompt_message: Optional[str] = None,
    **kwargs,
):
    return PydanticField(
        default,
        alias=alias,
        title=title,
        description=description,
        prompt_message=prompt_message,
        **kwargs,
    )


class CliArgs(BaseModel):
    show_help: bool = False
    tool: PositionalArg[Optional[str]] = None
    env: PositionalArg[Optional[str]] = None

    extra_args: Optional[Dict[str, Union[list, bool, int, str]]] = None
    raw_extra_args: Optional[List[str]] = None
    total_args: int

    def as_list(self):
        return [str(x) for x in [self.tool, self.env] if x] + (
            self.raw_extra_args if self.raw_extra_args else []
        )

    def as_str(self):
        return " ".join(self.as_list())

    def count(self):
        return self.total_args

    @pydantic_validator("tool", "env")
    def validate(cls, v, field):
        if v and not re.match("^[a-zA-Z0-9\\-_]+$", v.value):
            raise ValueError(
                f"{field.name} must be a string and not contain special characters"
            )
        return v

    @staticmethod
    def key_value_arg(key, arg):
        return f"{key}={arg}"


class ToolArgs(BaseModel):
    __tracer__ = None
    __prompt__ = None
    __fields_traced__ = set()

    show_help: bool = False
    extra_args: Optional[Dict[str, Union[list, bool, int, str]]] = None
    raw_extra_args: Optional[List[str]] = None

    def __getattribute__(self, item, skip_trace=False):
        if item == "__fields__":
            return super().__getattribute__(item)
        if item in self.__fields__:
            if skip_trace or not self.__config__.trace_on_access:
                return super().__getattribute__(item)

            if not self.__tracer__:
                raise Exception("Tracer not set")

            field = self.__fields__[item]
            value_ = self.__getattribute__(item, skip_trace=True)

            if value_ is None and self.__config__.prompt_on_access:
                return self.prompt(field)

            if item not in self.__fields_traced__ and item in self.__fields_set__:
                if field.type_ == PositionalArg:
                    self.__tracer__.tracing(value_.value)
                elif field.type_ == OptionalArg:
                    n, a = OptionalArg.cli_repr(field)
                    self.__tracer__.tracing(value_.value, key=n, key_alias=a)
                self.__fields_traced__.add(item)

        return super().__getattribute__(item)

    def prompt(self, field: Union[ModelField, str], **kwargs):
        if not self.__prompt__:
            raise Exception("Prompt not set")

        model_field = (
            field if isinstance(field, ModelField) else self.__fields__.get(field)
        )
        if not model_field:
            raise Exception(
                f"argument field must be a field name or a ModelField instance, got {field}"
            )

        value_ = self.__prompt__.query_field(
            model_field, model_class=self.__class__, **kwargs
        )

        self.__setattr__(model_field.name, value_)
        getattribute__ = self.__getattribute__(
            field, skip_trace=not self.__config__.trace_on_prompt
        )
        return getattribute__.value

    def _with_tracer(self, tracer):
        self.__tracer__ = tracer
        return self

    def _with_prompt(self, prompt):
        self.__prompt__ = prompt
        return self

    class Config:
        # pydantic config
        underscore_attrs_are_private = True
        validate_assignment = True

        # hexagon config
        trace_on_access = True
        trace_on_prompt = True
        prompt_on_access = False

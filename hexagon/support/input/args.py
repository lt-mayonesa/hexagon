import abc
from copy import copy
from inspect import isclass
from typing import Optional, Dict, Union, List, TypeVar, Generic, Any, Callable

from pydantic import (
    BaseModel,
    ValidationError,
    Field as PydanticField,
)
from pydantic.fields import ModelField

ARGUMENT_KEY_PREFIX = "-"


T = TypeVar("T")


def name_key(name: str):
    return f"{ARGUMENT_KEY_PREFIX * 2}{name}"


def alias_key(alias: str):
    return f"{ARGUMENT_KEY_PREFIX}{alias}"


def bool_negated_key(name: str):
    return f"{ARGUMENT_KEY_PREFIX * 2}no-{name}"


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


# noinspection PyPep8Naming
def Arg(
    default: Any = None,
    *,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    prompt_default: Optional[Union[Any, Callable[[Any], Any]]] = None,
    prompt_message: Optional[Union[str, Callable[[Any], str]]] = None,
    prompt_instruction: Optional[str] = None,
    searchable: bool = False,
    **kwargs,
):
    """
    Used to provide extra information about an argument, either for the model schema or complex validation.
    Some arguments apply only to number fields (``int``, ``float``, ``Decimal``) and some apply only to ``str``.

    TODO: add support for `validators` kwarg
    """
    return PydanticField(
        default,
        alias=alias,
        title=title,
        description=description,
        prompt_default=prompt_default,
        prompt_message=prompt_message,
        prompt_instruction=prompt_instruction,
        searchable=searchable,
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

    @staticmethod
    def key_value_arg(key, arg):
        return f"{key}={arg}"

    @property
    def format_friendly_extra_args(self):
        return (
            {
                "positional": sorted(
                    [v for k, v in self.extra_args.items() if k.isdigit()]
                ),
                "optional": {
                    k: v for k, v in self.extra_args.items() if not k.isdigit()
                },
            }
            if self.extra_args
            else {}
        )


class ToolArgs(BaseModel):
    __tracer__ = None
    __prompt__ = None
    __fields_traced__ = set()

    show_help: bool = False
    extra_args: Optional[Dict[str, Union[list, bool, int, str]]] = None
    raw_extra_args: Optional[List[str]] = None

    def __init__(self, **data):
        for v in self.__fields__.values():
            if (
                isclass(v.type_) and issubclass(v.type_, HexagonArg)
            ) and not isinstance(v.default, HexagonArg):
                v.default = (
                    PositionalArg(v.default)
                    if v.type_ == PositionalArg
                    else OptionalArg(v.default)
                )
        super().__init__(**data)

    def __getattribute__(self, item, just_get=False):
        if just_get:
            return super().__getattribute__(item)
        if item == "__fields__":
            return super().__getattribute__(item)
        if item in self.__fields__:
            field = self.__fields__[item]
            value_ = self.__getattribute__(item, just_get=True)

            if (
                hasattr(value_, "__value__")
                and value_.__value__ is None
                and self.__config__.prompt_on_access
            ):
                self.prompt(field)
                return self.__getattribute__(item, just_get=True)

        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        arg = self.__getattribute__(key, just_get=True)
        if isinstance(arg, HexagonArg):
            # noinspection PyProtectedMember
            arg._init_refs(self, self.__fields__.get(key))

    def trace(self, field: Union[ModelField, str], retrace=False):
        if not self.__tracer__:
            raise ValueError("Tracer not initialized. Did _with_tracer() get called?")

        model_field = (
            field if isinstance(field, ModelField) else self.__fields__.get(field)
        )
        if not model_field:
            raise ValueError(
                f"field [{field}] not found, must be a field name or a ModelField instance"
            )

        if not self.__config__.trace_on_access:
            return

        value_ = self.__getattribute__(model_field.name, just_get=True)

        if (
            retrace or model_field.name not in self.__fields_traced__
        ) and model_field.name in self.__fields_set__:
            if model_field.type_ == PositionalArg:
                self.__tracer__.tracing(f"arg_{model_field.name}", value_.__value__)
            elif model_field.type_ == OptionalArg:
                n, a = OptionalArg.cli_repr(model_field)
                self.__tracer__.tracing(
                    f"arg_{model_field.name}", value_.__value__, key=n, key_alias=a
                )
            self.__fields_traced__.add(model_field.name)

    def prompt(
        self,
        field: Union[ModelField, str],
        skip_trace: Union[bool, Callable] = False,
        **kwargs,
    ):
        if not self.__prompt__:
            raise ValueError("prompt not initialized. Did _with_prompt() get called?")

        model_field = (
            field if isinstance(field, ModelField) else self.__fields__.get(field)
        )
        if not model_field:
            raise ValueError(
                f"field [{field}] not found, must be a field name or a ModelField instance"
            )

        value_ = self.__prompt__.query_field(
            model_field, model_class=self.__class__, **kwargs
        )

        self.__setattr__(model_field.name, value_)
        getattribute__ = self.__getattribute__(model_field.name)

        if callable(skip_trace):
            skip_trace = skip_trace(value_)

        if not skip_trace and self.__config__.trace_on_prompt:
            self.trace(model_field, retrace=not skip_trace)

        return getattribute__.__value__

    def _with_tracer(self, tracer):
        self.__tracer__ = tracer
        for k, field in self.__fields__.items():
            arg = self.__getattribute__(k, just_get=True)
            if isinstance(arg, HexagonArg):
                # noinspection PyProtectedMember
                arg._init_refs(self, field)
        return self

    def _with_prompt(self, prompt):
        self.__prompt__ = prompt
        for k, field in self.__fields__.items():
            arg = self.__getattribute__(k, just_get=True)
            if isinstance(arg, HexagonArg):
                # noinspection PyProtectedMember
                arg._init_refs(self, field)
        return self

    class Config:
        # pydantic config
        underscore_attrs_are_private = True
        validate_assignment = True

        # hexagon config
        trace_on_access = True
        trace_on_prompt = True
        prompt_on_access = False

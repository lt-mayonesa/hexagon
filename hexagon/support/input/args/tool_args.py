from inspect import isclass
from typing import Optional, Dict, Union, List, Callable

from pydantic import BaseModel
from pydantic.fields import ModelField

from hexagon.support.input.args import HexagonArg
from hexagon.support.input.args.hexagon_args import PositionalArg, OptionalArg


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

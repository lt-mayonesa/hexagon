from inspect import isclass
from typing import Optional, Dict, Union, List, Callable, get_origin

from pydantic import BaseModel

from hexagon.support.input.args import HexagonArg
from hexagon.support.input.args.field_reference import FieldReference
from hexagon.support.input.args.hexagon_args import PositionalArg, OptionalArg


class ToolArgs(BaseModel):
    model_config = {
        # pydantic config
        "validate_assignment": True,
        # hexagon config
        "trace_on_access": True,
        "trace_on_prompt": True,
        "prompt_on_access": False,
    }
    __tracer__ = None
    __prompt__ = None
    __fields_traced__ = set()
    __fields_initialized__ = set()
    __track_fields_set__ = False

    show_help: bool = False
    extra_args: Optional[Dict[str, Union[list, bool, int, str]]] = None
    raw_extra_args: Optional[List[str]] = None

    def __init__(self, **data):
        for _k, v in self.model_fields.items():
            if (
                isclass(get_origin(v.annotation))
                and issubclass(get_origin(v.annotation), HexagonArg)
            ) and not isinstance(v.default, HexagonArg):
                v.default = (
                    PositionalArg(v.default)
                    if v.annotation == PositionalArg
                    else OptionalArg(v.default)
                )
        super().__init__(**data)
        self.__fields_initialized__ = set(self.model_fields_set)
        # for each self.model_field that is not a HexagonArg, convert it to a HexagonArg
        for k, v in self.model_fields.items():
            if k in ["show_help", "extra_args", "raw_extra_args"]:
                continue
            value_ = self.__getattribute__(k, just_get=True)
            if not isinstance(value_, HexagonArg):
                self.__setattr__(
                    k,
                    (
                        PositionalArg(value_)
                        if get_origin(v.annotation) == PositionalArg
                        else OptionalArg(value_)
                    ),
                )
        self.__track_fields_set__ = True

    def __getattribute__(self, item, just_get=False):
        if just_get:
            return super().__getattribute__(item)
        if item == "model_fields":
            return super().__getattribute__(item)
        if item in self.model_fields:
            field = self.model_fields[item]
            value_ = self.__getattribute__(item, just_get=True)

            if (
                hasattr(value_, "__value__")
                and value_.__value__ is None
                and self.model_config["prompt_on_access"]
            ):
                self.prompt(FieldReference(item, field))
                return self.__getattribute__(item, just_get=True)

        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        arg = self.__getattribute__(key, just_get=True)
        if isinstance(arg, HexagonArg):
            # noinspection PyProtectedMember
            arg._init_refs(self, FieldReference(key, self.model_fields.get(key)))
        if self.__track_fields_set__:
            self.__fields_initialized__.add(key)

    def trace(self, field: Union[FieldReference, str], retrace=False):
        if not self.__tracer__:
            raise ValueError("Tracer not initialized. Did _with_tracer() get called?")

        model_field = (
            field
            if isinstance(field, FieldReference)
            else self.model_fields.get(field.name)
        )
        if not model_field:
            raise ValueError(
                f"field [{field}] not found, must be a field name or a FieldReference instance"
            )

        if not self.model_config["trace_on_access"]:
            return

        value_ = self.__getattribute__(model_field.name, just_get=True)

        if (
            retrace or model_field.name not in self.__fields_traced__
        ) and model_field.name in self.__fields_initialized__:
            if get_origin(model_field.info.annotation) == PositionalArg:
                self.__tracer__.tracing(f"arg_{model_field.name}", value_.__value__)
            elif get_origin(model_field.info.annotation) == OptionalArg:
                n, a = OptionalArg.cli_repr(model_field)
                self.__tracer__.tracing(
                    f"arg_{model_field.name}", value_.__value__, key=n, key_alias=a
                )
            self.__fields_traced__.add(model_field.name)

    def prompt(
        self,
        field: Union[FieldReference, str],
        skip_trace: Union[bool, Callable] = False,
        **kwargs,
    ):
        if not self.__prompt__:
            raise ValueError("prompt not initialized. Did _with_prompt() get called?")

        model_field = (
            field
            if isinstance(field, FieldReference)
            else self.model_fields.get(field.name)
        )
        if not model_field:
            raise ValueError(
                f"field [{field}] not found, must be a field name or a FieldReference instance"
            )

        value_ = self.__prompt__.query_field(
            model_field, model_class=self.__class__, **kwargs
        )

        self.__setattr__(model_field.name, value_)
        getattribute__ = self.__getattribute__(model_field.name)

        if callable(skip_trace):
            skip_trace = skip_trace(value_)

        if not skip_trace and self.model_config["trace_on_prompt"]:
            self.trace(model_field, retrace=not skip_trace)

        return getattribute__.__value__

    def _with_tracer(self, tracer):
        self.__tracer__ = tracer
        for k, field in self.model_fields.items():
            arg = self.__getattribute__(k, just_get=True)
            if isinstance(arg, HexagonArg):
                # noinspection PyProtectedMember
                arg._init_refs(self, FieldReference(k, field))
        return self

    def _with_prompt(self, prompt):
        self.__prompt__ = prompt
        for k, field in self.model_fields.items():
            arg = self.__getattribute__(k, just_get=True)
            if isinstance(arg, HexagonArg):
                # noinspection PyProtectedMember
                arg._init_refs(self, FieldReference(k, field))
        return self

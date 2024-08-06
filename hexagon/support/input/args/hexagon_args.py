import abc
from typing import Generic, Union, Callable, TypeVar, get_args, Any, get_origin

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_core.core_schema import ValidatorFunctionWrapHandler

from hexagon.support.input.args.field_reference import FieldReference

ARGUMENT_KEY_PREFIX = "-"

T = TypeVar("T")


class HexagonArg(Generic[T]):
    __model__ = None
    __field__ = None

    def __init__(self, value: T):
        self.__value__ = value

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

    def _init_refs(self, model: Any, field: FieldReference):
        self.__field__ = field
        self.__model__ = model

    @staticmethod
    @abc.abstractmethod
    def cli_repr(field: FieldReference):
        return

    def __str__(self, **kwargs):
        return str(self.__value__)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        origin = get_origin(source_type)
        if origin is None:  # used as `x: Owner` without params
            origin = source_type
            item_tp = Any
        else:
            item_tp = get_args(source_type)[0]
        # both calling handler(...) and handler.generate_schema(...)
        # would work, but prefer the latter for conceptual and consistency reasons
        item_schema = handler.generate_schema(item_tp)

        def val_item(v: Any, handler: ValidatorFunctionWrapHandler) -> HexagonArg[Any]:
            if not isinstance(v, cls):
                v = cls(handler(v))
            return v

        python_schema = core_schema.chain_schema(
            # `chain_schema` means do the following steps in order:
            [
                # # Ensure the value is an instance of HexagonArg
                # core_schema.is_instance_schema(cls),
                # Use the item_schema to validate `items`
                core_schema.no_info_wrap_validator_function(val_item, item_schema),
            ]
        )

        return core_schema.json_or_python_schema(
            # for JSON accept an object with name and item keys
            json_schema=core_schema.chain_schema(
                [
                    item_schema,
                    # after validating the json data convert it to python
                    core_schema.no_info_before_validator_function(
                        lambda v: cls(v),
                        # note that we re-use the same schema here as below
                        python_schema,
                    ),
                ]
            ),
            python_schema=python_schema,
        )


class PositionalArg(HexagonArg[T]):
    @staticmethod
    def cli_repr(field: FieldReference):
        return field.name, None


class OptionalArg(HexagonArg[T]):
    @staticmethod
    def cli_repr(field: FieldReference):
        def initials():
            return "".join([w[0] for w in field.name.split("_")])

        return (
            name_key(field.name.replace("_", "-")),
            alias_key(
                field.info.alias.replace("_", "-")
                if field.info.alias and field.info.alias != field.name
                else initials()
            ),
        )


def name_key(name: str):
    return f"{ARGUMENT_KEY_PREFIX * 2}{name}"


def alias_key(alias: str):
    return f"{ARGUMENT_KEY_PREFIX}{alias}"

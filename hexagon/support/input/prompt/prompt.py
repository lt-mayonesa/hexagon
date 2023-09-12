from copy import copy
from enum import Enum, auto
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base import Choice
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator
from pydantic import ValidationError as PydanticValidationError, DirectoryPath
from pydantic.fields import ModelField, Validator as PydanticValidator

from hexagon.runtime.singletons import options
from hexagon.support.input.args import HexagonArg
from hexagon.support.input.prompt.for_all_methods import for_all_methods
from hexagon.support.input.prompt.hints import HintsBuilder
from hexagon.support.output.printer import log
from hexagon.utils.typing import field_info


class PromptValidator(Validator):
    def __init__(self, validators, cls):
        self.validators = validators
        self.cls = cls

    def validate(self, document: Document) -> None:
        try:
            for validator in self.validators.values():
                validator.func(self.cls, document.text)
        except PydanticValidationError as e:
            raise ValidationError(
                message=" / ".join([x["msg"] for x in e.errors()]),
                cursor_position=len(document.text),
            )
        except ValueError as e:
            raise ValidationError(message=e.args[0], cursor_position=len(document.text))


def default_validator(model_field: ModelField, mapper=lambda x: x):
    def func(cls, value):
        value, error = model_field.sub_fields[0].validate(mapper(value), {}, loc="")
        if error:
            raise PydanticValidationError([error], model=cls)
        return value

    return func


def list_mapper(v):
    return v.strip().split("\n")


def set_default(options, model_field: ModelField):
    if "default" in options:
        return {"default": options["default"]}
    elif model_field.default:
        default = (
            model_field.default.value
            if isinstance(model_field.default, HexagonArg)
            else model_field.default
        )
        if default is not None:
            return {"default": default}

    return {}


class InquiryType(Enum):
    STRING = auto()
    STRING_SEARCHABLE = auto()
    STRING_LIST = auto()
    STRING_LIST_SEARCHABLE = auto()
    ENUM = auto()
    ENUM_SEARCHABLE = auto()
    ENUM_LIST = auto()
    ENUM_LIST_SEARCHABLE = auto()
    PATH = auto()
    PATH_SEARCHABLE = auto()
    INT = auto()
    FLOAT = auto()
    SECRET = auto()


def _determine_expected_inquiry(
    iterable, of_enum, type_, declaration_extras, invocation_extras
) -> (InquiryType, dict):
    """
    TODO: move this to a separate module and unit test it
    """
    extras = {**declaration_extras, **invocation_extras}
    searchable = extras.get("searchable", False)

    query = InquiryType.STRING if not searchable else InquiryType.STRING_SEARCHABLE
    if iterable and of_enum:
        query = (
            InquiryType.ENUM_LIST
            if not searchable
            else InquiryType.ENUM_LIST_SEARCHABLE
        )
    elif iterable:
        query = (
            InquiryType.STRING_LIST
            if not searchable
            else InquiryType.STRING_LIST_SEARCHABLE
        )
    elif of_enum:
        query = InquiryType.ENUM if not searchable else InquiryType.ENUM_SEARCHABLE
    elif issubclass(type_, Path):
        query = InquiryType.PATH if not searchable else InquiryType.PATH_SEARCHABLE
    elif issubclass(type_, int):
        query = InquiryType.INT
    elif issubclass(type_, float):
        query = InquiryType.FLOAT
    elif extras.get("secret", False):
        query = InquiryType.SECRET

    return query, extras


def setup_enum_list(self, args, extras, inquiry_type, type_):
    args["choices"] = [
        Choice(
            name=x.name,
            value=x,
            enabled=("default" in args and x in args["default"]),
        )
        for x in type_.__args__[0]
    ]
    if inquiry_type == InquiryType.ENUM_LIST_SEARCHABLE:
        args["multiselect"] = True
        return self.fuzzy, lambda x: x
    else:
        return self.checkbox, lambda x: x


def setup_string_list(self, args, extras, inquiry_type, type_):
    mapper = list_mapper
    args["filter"] = mapper
    args["instruction"] = (
        args["instruction"]
        or "(each line represents a value) ESC + Enter to finish input"
    )
    args["multiline"] = True
    return self.text, mapper


def setup_enum(self, args, extras, inquiry_type, type_):
    args["choices"] = [{"name": x.name, "value": x} for x in type_]
    if inquiry_type == InquiryType.ENUM_SEARCHABLE:
        args["default"] = args["default"].value
        return self.fuzzy, lambda x: x
    else:
        args["default"] = args["default"]
        return self.select, lambda x: x


def setup_searchable_list(self, args, extras, inquiry_type, type_):
    args["choices"] = extras["choices"]
    if inquiry_type == InquiryType.STRING_LIST_SEARCHABLE:
        args["multiselect"] = True
    return self.fuzzy, lambda x: x


def setup_path(self, args, extras, inquiry_type, type_):
    if inquiry_type == InquiryType.PATH_SEARCHABLE:
        if "glob" in extras:
            args["choices"] = sorted(
                Path(extras.get("cwd", ".")).rglob(extras["glob"]), key=lambda x: x.name
            )
        elif "choices" in extras:
            args["choices"] = extras["choices"]
        else:
            raise ValueError("searchable path must have either glob or choices defined")
        return self.fuzzy, lambda x: x
    else:
        args["only_directories"] = (
            args["only_directories"]
            if "only_directories" in args
            else issubclass(type_, DirectoryPath)
        )
        return self.path, lambda x: x


def setup_int(self, args, extras, inquiry_type, type_):
    return self.number, lambda x: x


def setup_float(self, args, extras, inquiry_type, type_):
    args["float_allowed"] = True
    return self.number, lambda x: x


def setup_secret(self, args, extras, inquiry_type, type_):
    return self.secret, lambda x: x


def setup_string(self, args, extras, inquiry_type, type_):
    return self.text, lambda x: x


@for_all_methods(log.status_aware, exclude=["query_field"])
class Prompt:
    def query_field(self, model_field: ModelField, model_class, **kwargs):
        # TODO: this method is a mess, refactor it
        declaration_extras = copy(model_field.field_info.extra)
        invocation_extras = copy(kwargs)
        args = {
            "message": declaration_extras.get("prompt_message", None)
            or f"Enter {model_field.name}:",
            "instruction": declaration_extras.get("prompt_instruction", None),
        }
        args.update(set_default(invocation_extras, model_field))

        type_, iterable, of_enum = field_info(model_field)

        inquiry_type, extras = _determine_expected_inquiry(
            iterable, of_enum, type_, declaration_extras, invocation_extras
        )

        setups = {
            InquiryType.ENUM_LIST: setup_enum_list,
            InquiryType.ENUM_LIST_SEARCHABLE: setup_enum_list,
            InquiryType.STRING_LIST: setup_string_list,
            InquiryType.STRING_LIST_SEARCHABLE: setup_searchable_list,
            InquiryType.ENUM: setup_enum,
            InquiryType.ENUM_SEARCHABLE: setup_enum,
            InquiryType.STRING_SEARCHABLE: setup_searchable_list,
            InquiryType.PATH: setup_path,
            InquiryType.PATH_SEARCHABLE: setup_path,
            InquiryType.INT: setup_int,
            InquiryType.FLOAT: setup_float,
            InquiryType.SECRET: setup_secret,
        }

        inq, mapper = setups.get(inquiry_type, setup_string)(
            self, args, extras, inquiry_type, type_
        )

        if model_field.sub_fields:
            validators_ = {
                "default": PydanticValidator(
                    default_validator(model_field, mapper=mapper), check_fields=True
                )
            }
            if model_field.class_validators:
                validators_.update(
                    {
                        **model_field.class_validators,
                    }
                )
            args["validate"] = PromptValidator(
                validators_,
                model_class,
            )

        # FIXME: this is working by chance, it's not the best way to do it
        if "searchable" in invocation_extras:
            del invocation_extras["searchable"]
        args.update(**invocation_extras)
        return inq(**args)

    @staticmethod
    def text(**kwargs):
        if not options.hints_disabled:
            kwargs["long_instruction"] = (
                HintsBuilder().with_enter_cancel_skip().with_autocomplete().build()
            )
        return inquirer.text(**kwargs).execute()

    @staticmethod
    def select(**kwargs):
        if not options.hints_disabled:
            kwargs["long_instruction"] = (
                HintsBuilder().with_enter_cancel_skip().with_vertical_movement().build()
            )
        return inquirer.select(**kwargs).execute()

    @staticmethod
    def checkbox(**kwargs):
        if not options.hints_disabled:
            kwargs["long_instruction"] = (
                HintsBuilder()
                .with_enter_cancel_skip()
                .with_vertical_movement()
                .with_select_toggles()
                .build()
            )
        return inquirer.checkbox(**kwargs).execute()

    @staticmethod
    def confirm(*args, **kwargs):
        if not options.hints_disabled:
            # not adding confirm_letter and reject_letter as hints because it seems redundant
            kwargs["long_instruction"] = HintsBuilder().with_enter_cancel_skip().build()
        return inquirer.confirm(*args, **kwargs).execute()

    @staticmethod
    def fuzzy(**kwargs):
        kwargs["keybindings"] = {
            "toggle-exact": [
                {"key": "c-f"}
            ]  # toggle string matching algorithm between fuzzy or exact
        }
        if not options.hints_disabled:
            builder = (
                HintsBuilder()
                .with_enter_cancel_skip()
                .with_vertical_movement()
                .with_fuzzy_toggle()
            )
            if "multiselect" in kwargs:
                builder.with_select_toggles()
            kwargs["long_instruction"] = builder.build()
        return inquirer.fuzzy(border=log.use_borders(), **kwargs).execute()

    @staticmethod
    def path(**kwargs):
        if not options.hints_disabled:
            kwargs["long_instruction"] = (
                HintsBuilder().with_enter_cancel_skip().with_autocomplete().build()
            )
        return inquirer.filepath(**kwargs).execute()

    @staticmethod
    def number(**kwargs):
        if not options.hints_disabled:
            builder = HintsBuilder().with_enter_cancel_skip().with_number_controls()
            if "float_allowed" in kwargs:
                builder.with_floating_point()
            kwargs["long_instruction"] = builder.build()
        return inquirer.number(**kwargs).execute()

    @staticmethod
    def secret(**kwargs):
        if not options.hints_disabled:
            kwargs["long_instruction"] = HintsBuilder().with_enter_cancel_skip().build()
        return inquirer.secret(**kwargs).execute()
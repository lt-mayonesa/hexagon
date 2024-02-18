import re
from copy import copy
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, Literal, Callable, List

from InquirerPy import inquirer
from InquirerPy.base import Choice
from InquirerPy.utils import run_in_terminal
from prompt_toolkit.buffer import ValidationState
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator
from pydantic import ValidationError as PydanticValidationError, DirectoryPath
from pydantic.fields import ModelField, Validator as PydanticValidator

from hexagon.domain.hexagon_error import ListHexagonError
from hexagon.runtime.singletons import options
from hexagon.support.input.args import HexagonArg
from hexagon.support.input.prompt.for_all_methods import for_all_methods
from hexagon.support.input.prompt.hints import HintsBuilder
from hexagon.support.input.types import path_validator
from hexagon.support.output.printer import log
from hexagon.utils.typing import field_info


class HexagonArgumentSetupError(ListHexagonError):
    def __init__(self, argument: str, prop: str):
        super().__init__(
            [
                _("error.support.input.prompt.prompt.invalid_argument_setup").format(
                    argument=argument, property=prop
                ),
            ]
        )


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
        value, error = model_field.validate(mapper(value), {}, loc="")
        if error:
            raise PydanticValidationError([error], model=cls)
        return value

    return func


def list_mapper(v):
    return v.strip().split("\n")


def set_default(invocation_extras, model_field: ModelField):
    if model_field.field_info.extra.get("prompt_default"):
        return {"default": model_field.field_info.extra["prompt_default"]}
    if "default" in invocation_extras:
        return {"default": invocation_extras["default"]}
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
    BOOLEAN = auto()


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
    elif issubclass(type_, bool):
        query = InquiryType.BOOLEAN
    elif issubclass(type_, int):
        query = InquiryType.INT
    elif issubclass(type_, float):
        query = InquiryType.FLOAT
    elif extras.get("secret", False):
        query = InquiryType.SECRET

    return query, extras


@for_all_methods(log.status_aware, exclude=["query_field"])
class Prompt:
    def query_field(self, model_field: ModelField, model_class, **kwargs):
        # TODO: this method is a mess, refactor it
        declaration_extras = copy(model_field.field_info.extra)
        invocation_extras = copy(kwargs)
        inquiry_args = {
            "message": declaration_extras.get("prompt_message", None)
            or f"Enter {model_field.name}:",
            "instruction": declaration_extras.get("prompt_instruction", None),
        }
        inquiry_args.update(set_default(invocation_extras, model_field))

        field_type, iterable, of_enum = field_info(model_field)

        inquiry_type, extras = _determine_expected_inquiry(
            iterable, of_enum, field_type, declaration_extras, invocation_extras
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
            InquiryType.BOOLEAN: setup_bool,
        }

        inq, mapper = setups.get(inquiry_type, setup_string)(
            self,
            inquiry_args=inquiry_args,
            inquiry_type=inquiry_type,
            extras=extras,
            field_type=field_type,
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
            inquiry_args["validate"] = PromptValidator(
                validators_,
                model_class,
            )

        # FIXME: this is working by chance, it's not the best way to do it
        if "searchable" in invocation_extras:
            del invocation_extras["searchable"]

        inquiry_args.update(**invocation_extras)
        try:
            return inq(**inquiry_args)
        except TypeError as e:
            if "__init__() got an unexpected keyword argument" in e.args[0]:
                prop = re.search(".*\s('\w+')$", e.args[0]).group(1).strip()
                err = HexagonArgumentSetupError(model_field.name, prop)
            else:
                raise e

        if err:
            raise err

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
        if "validate" in kwargs:
            del kwargs["validate"]  # validate is not supported by confirm
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
        is_dir = kwargs.get("only_directories", False)
        if not options.hints_disabled:
            hints = HintsBuilder().with_enter_cancel_skip().with_autocomplete()
            if is_dir:
                hints.with_path_support()
            kwargs["long_instruction"] = hints.build()
        filepath_prompt = inquirer.filepath(**kwargs)

        if is_dir:
            # noinspection PyProtectedMember
            @filepath_prompt.register_kb(options.keymap.create_dir)
            def _create_dir(__):
                path = path_validator(filepath_prompt._session.default_buffer.text)
                if not path.exists():
                    try:
                        path.mkdir(parents=True)
                        run_in_terminal(
                            lambda: log.info(
                                _("msg.support.prompt.prompt.directory_created").format(
                                    path=path.absolute()
                                )
                            )
                        )
                        filepath_prompt._session.default_buffer.validation_state = (
                            ValidationState.INVALID
                        )
                        filepath_prompt._session.default_buffer.validation_error = None
                    except Exception as e:
                        filepath_prompt._set_error(str(e))

        return filepath_prompt.execute()

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


def setup_enum_list(
    self: Prompt,
    inquiry_type: Literal[InquiryType.ENUM_LIST, InquiryType.ENUM_LIST_SEARCHABLE],
    inquiry_args: Dict[str, Any],
    field_type: Any,
    **_,
) -> (Callable, Callable):
    inquiry_args["choices"] = [
        Choice(
            name=x.name,
            value=x,
            enabled=("default" in inquiry_args and x in inquiry_args["default"]),
        )
        for x in field_type.__args__[0]
    ]
    inquiry_args["default"] = ""
    if inquiry_type == InquiryType.ENUM_LIST_SEARCHABLE:
        inquiry_args["multiselect"] = True
        return self.fuzzy, lambda x: x
    else:
        return self.checkbox, lambda x: x


def setup_string_list(
    self: Prompt, inquiry_args: Dict[str, Any], **_
) -> (Callable, Callable):
    mapper = list_mapper
    inquiry_args["filter"] = mapper
    inquiry_args["instruction"] = (
        inquiry_args["instruction"]
        or "(each line represents a value) ESC + Enter to finish input"
    )
    inquiry_args["multiline"] = True
    return self.text, mapper


def setup_enum(
    self: Prompt,
    inquiry_type: Literal[InquiryType.ENUM, InquiryType.ENUM_SEARCHABLE],
    inquiry_args: Dict[str, Any],
    field_type: Any,
    **_,
) -> (Callable, Callable):
    inquiry_args["choices"] = [{"name": x.name, "value": x} for x in field_type]
    if inquiry_type == InquiryType.ENUM_SEARCHABLE:
        inquiry_args["default"] = (
            inquiry_args["default"].value if "default" in inquiry_args else None
        )
        return self.fuzzy, lambda x: x
    else:
        return self.select, lambda x: x


def setup_searchable_list(
    self: Prompt,
    inquiry_type: Literal[
        InquiryType.STRING_SEARCHABLE, InquiryType.STRING_LIST_SEARCHABLE
    ],
    inquiry_args: Dict[str, Any],
    extras: Dict[str, Any],
    **_,
) -> (Callable, Callable):
    inquiry_args["choices"] = extras["choices"]
    if inquiry_type == InquiryType.STRING_LIST_SEARCHABLE:
        inquiry_args["multiselect"] = True
    return self.fuzzy, lambda x: x


def setup_path(
    self: Prompt,
    inquiry_type: Literal[InquiryType.PATH, InquiryType.PATH_SEARCHABLE],
    inquiry_args: Dict[str, Any],
    extras: Dict[str, Any],
    field_type: Any,
) -> (Callable, Callable):
    if inquiry_type == InquiryType.PATH_SEARCHABLE:
        choices: List[Dict[str, Any] or Any] = []
        if "glob_extra_choices" in extras:
            extra_choices = extras["glob_extra_choices"]
            for choice in extra_choices:
                choices.append(
                    choice
                    if isinstance(choice, dict)
                    else {
                        "name": choice,
                        "value": choice,
                    }
                )

        if "glob" in extras:
            choices = choices + [
                f
                for f in sorted(
                    Path(extras.get("cwd", ".")).rglob(extras["glob"]),
                    key=lambda x: x.name,
                )
            ]
        elif "choices" in extras:
            choices = choices + extras["choices"]
        else:
            raise ValueError("searchable path must have either glob or choices defined")
        inquiry_args["choices"] = choices
        return self.fuzzy, lambda x: x
    else:
        inquiry_args["only_directories"] = (
            inquiry_args["only_directories"]
            if "only_directories" in inquiry_args
            else issubclass(field_type, DirectoryPath)
        )
        return self.path, lambda x: x


def setup_int(self: Prompt, **_) -> (Callable, Callable):
    return self.number, lambda x: x


def setup_float(
    self: Prompt, inquiry_args: Dict[str, Any], **_
) -> (Callable, Callable):
    inquiry_args["float_allowed"] = True
    return self.number, lambda x: x


def setup_secret(self: Prompt, **_) -> (Callable, Callable):
    return self.secret, lambda x: x


def setup_string(self: Prompt, **_) -> (Callable, Callable):
    return self.text, lambda x: x


def setup_bool(self: Prompt, **_) -> (Callable, Callable):
    return self.confirm, lambda x: x

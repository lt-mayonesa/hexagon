from pathlib import Path
from typing import Callable, Any

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


@for_all_methods(log.status_aware, exclude=["query_field"])
class Prompt:
    def query_field(self, model_field: ModelField, model_class, **kwargs):
        inq = self.text
        args = {
            "message": model_field.field_info.extra.get("prompt_message", None)
            or f"Enter {model_field.name}:",
            "instruction": model_field.field_info.extra.get("prompt_instruction", None),
        }
        args.update(set_default(kwargs, model_field))

        type_, iterable, of_enum = field_info(model_field)

        mapper: Callable[[Any], Any] = lambda x: x

        # TODO: add support for inquirer.secret and inquirer.number
        if iterable and of_enum:
            args["choices"] = [
                Choice(
                    name=x.name,
                    value=x,
                    enabled=("default" in args and x in args["default"]),
                )
                for x in type_.__args__[0]
            ]
            inq = self.checkbox
        elif iterable and "choices" not in kwargs:
            mapper = list_mapper
            args["filter"] = mapper
            args["instruction"] = (
                args["instruction"]
                or "(each line represents a value) ESC + Enter to finish input"
            )
            args["multiline"] = True
            inq = self.text
        elif of_enum:
            args["choices"] = [{"name": x.name, "value": x} for x in type_]
            inq = self.select
        elif "choices" in kwargs:
            # TODO: add better logic for using fuzzy prompt
            args["choices"] = kwargs["choices"]
            if iterable:
                args["multiselect"] = True
            inq = self.fuzzy
        elif issubclass(type_, Path):
            args["only_directories"] = (
                args["only_directories"]
                if "only_directories" in args
                else issubclass(type_, DirectoryPath)
            )
            inq = self.path

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
        args.update(**kwargs)
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

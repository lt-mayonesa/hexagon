from pathlib import Path
from typing import Callable, Any

from InquirerPy import inquirer
from InquirerPy.base import Choice
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator
from pydantic import ValidationError as PydanticValidationError
from pydantic.fields import ModelField, Validator as PydanticValidator

from hexagon.domain.args import HexagonArg
from hexagon.support.printer import log
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


class Prompt:
    def query_field(self, model_field: ModelField, model_class, **kwargs):
        inq = self.text
        args = {
            "message": model_field.field_info.extra.get("prompt_message", None)
            or f"Enter {model_field.name}:",
        }
        args.update(set_default(kwargs, model_field))

        type_, iterable, of_enum = field_info(model_field)

        mapper: Callable[[Any], Any] = lambda x: x

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
        elif iterable:
            mapper = list_mapper
            args["filter"] = mapper
            args["message"] = args["message"] + " (each line represents a value)"
            args["multiline"] = True
            inq = self.text
        elif of_enum:
            args["choices"] = [{"name": x.name, "value": x} for x in type_]
            inq = self.select
        elif "choices" in kwargs:
            # TODO: add better logic for using fuzzy prompt
            args["choices"] = kwargs["choices"]
            inq = self.fuzzy
        elif issubclass(type_, Path):
            args["message"] = args["message"] + " (relative to project root)"
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

        args.update(**kwargs)
        return inq(**args)

    @staticmethod
    def text(**kwargs):
        return inquirer.text(**kwargs).execute()

    @staticmethod
    def select(**kwargs):
        return inquirer.select(**kwargs).execute()

    @staticmethod
    def checkbox(**kwargs):
        return inquirer.checkbox(**kwargs).execute()

    @staticmethod
    def confirm(*args, **kwargs):
        return inquirer.confirm(*args, **kwargs).execute()

    @staticmethod
    def fuzzy(**kwargs):
        return inquirer.fuzzy(border=log.use_borders(), **kwargs).execute()

    @staticmethod
    def path(**kwargs):
        return inquirer.filepath(**kwargs).execute()


prompt = Prompt()

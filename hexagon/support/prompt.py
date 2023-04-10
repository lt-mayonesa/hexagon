from pathlib import Path

from InquirerPy import inquirer
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator
from pydantic.fields import ModelField

from hexagon.utils.typing import field_info


class PromptValidator(Validator):
    def __init__(self, validators, cls):
        self.validators = validators
        self.cls = cls

    def validate(self, document: Document) -> None:
        # FIXME: add validation based on field type's default validation
        try:
            for validator in self.validators.values():
                validator.func(self.cls, document.text)
        except ValueError as e:
            raise ValidationError(message=e.args[0], cursor_position=len(document.text))


class Prompt:
    def query_field(self, model_field: ModelField, model_class, **kwargs):
        inq = self.text
        args = {
            "message": model_field.field_info.extra.get("prompt_message", None)
            or f"Enter {model_field.name}:",
        }
        if model_field.default:
            args["default"] = model_field.default

        type_, iterable, of_enum = field_info(model_field)

        if model_field.class_validators:
            args["validate"] = PromptValidator(
                model_field.class_validators, model_class
            )

        if iterable and of_enum:
            # TODO: use inquirerpy's Choice class (need to update inquirerpy version)
            # noinspection PyTypedDict
            args["choices"] = [
                {
                    "name": x.name,
                    "value": x,
                    "enabled": ("default" in args and x in args["default"]),
                }
                for x in type_.__args__[0]
            ]
            inq = self.checkbox
        elif iterable:
            args["filter"] = lambda x: x.strip().split("\n")
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
        return inquirer.fuzzy(**kwargs).execute()

    @staticmethod
    def path(**kwargs):
        return inquirer.filepath(**kwargs).execute()


prompt = Prompt()

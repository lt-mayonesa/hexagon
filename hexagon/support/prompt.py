from InquirerPy import inquirer
from pydantic.fields import ModelField

from hexagon.utils.typing import field_info


class Prompt:
    def query_field(self, model_field: ModelField, **kwargs):
        inq = self.text
        args = {
            "message": model_field.field_info.extra.get("prompt_message", None)
            or f"Enter {model_field.name}:",
        }
        if model_field.default:
            args["default"] = model_field.default

        type_, iterable, of_enum = field_info(model_field)

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

        args.update(**kwargs)
        return inq(**args)

    @staticmethod
    def text(**kwargs) -> str:
        return inquirer.text(**kwargs).execute()

    @staticmethod
    def select(**kwargs) -> str:
        return inquirer.select(**kwargs).execute()

    @staticmethod
    def checkbox(**kwargs) -> str:
        return inquirer.checkbox(**kwargs).execute()

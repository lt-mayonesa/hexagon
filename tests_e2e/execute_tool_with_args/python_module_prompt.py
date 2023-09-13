from enum import Enum
from typing import Any, Optional, List

from pydantic import validator, FilePath

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg, PositionalArg, Arg
from hexagon.support.output.printer import log


class Category(str, Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"


class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed loaded automatically by hexagon
    """

    test: PositionalArg[str] = Arg(None)
    name: OptionalArg[str] = Arg(None, prompt_message="input the person's name:")
    age: OptionalArg[int] = None
    country: OptionalArg[str] = "Argentina"
    likes: OptionalArg[list] = None
    tag: OptionalArg[Category] = Category.C
    available_tags: OptionalArg[List[Category]] = [Category.B, Category.E]
    total_amount: OptionalArg[float] = None
    fuzzy_input: OptionalArg[str] = Arg(
        None,
        searchable=True,
        choices=["a sentence to match", "a sentence not to match", "something else"],
    )
    fuzzy_file_input: OptionalArg[FilePath] = Arg(None, searchable=True, glob="*.txt")

    @validator("age")
    def validate_age(cls, arg):
        if arg:
            v = int(arg) if isinstance(arg, str) else arg.value
            if v < 18:
                raise ValueError("age must be greater than 18")
        return arg

    @validator("age")
    def validate_age_max(cls, arg):
        if arg:
            v = int(arg) if isinstance(arg, str) else arg.value
            if v > 48:
                raise ValueError("age must be less than 48")
        return arg


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    cases = {
        "prompt_name_and_age": prompt_name_and_age,
        "prompt_validate_age": prompt_validate_age,
        "prompt_show_default_value": prompt_show_default_value,
        "prompt_list_value": prompt_list_value,
        "prompt_enum_choices": prompt_enum_choices,
        "prompt_list_enum_choices": prompt_list_enum_choices,
        "prompt_validate_type": prompt_validate_type,
        "prompt_fuzzy_search": prompt_fuzzy_search,
        "prompt_fuzzy_file": prompt_fuzzy_file,
        "prompt_multiple_times": prompt_multiple_times,
    }

    cases.get(cli_args.test.value, default)(cli_args)


def prompt_name_and_age(cli_args):
    log.result(f"name: {cli_args.name.prompt()}")
    log.result(f"age: {cli_args.age.prompt()}")
    log.result(f"age type: {type(cli_args.age.value).__name__}")


def prompt_validate_age(cli_args):
    log.result(f"age: {cli_args.age.prompt()}")


def prompt_show_default_value(cli_args):
    log.result(f"country: {cli_args.country.prompt()}")


def prompt_list_value(cli_args):
    log.result(f"likes: {cli_args.likes.prompt()}")


def prompt_enum_choices(cli_args):
    log.result(f"tag: {cli_args.tag.prompt().value}")
    log.result(f"tag type: {type(cli_args.tag.value).__name__}")


def prompt_list_enum_choices(cli_args):
    log.result(f"available_tags: {cli_args.available_tags.prompt()}")


def prompt_validate_type(cli_args):
    log.result(f"total_amount: {cli_args.total_amount.prompt()}")
    log.result(f"total_amount type: {type(cli_args.total_amount.value).__name__}")


def prompt_fuzzy_search(cli_args):
    log.result(f"fuzzy_input: {cli_args.fuzzy_input.prompt()}")
    log.result(
        f"fuzzy_input: {cli_args.fuzzy_input.prompt(choices=['another sentence to match', 'something else'])}"
    )


def prompt_fuzzy_file(cli_args):
    log.result(f"fuzzy_file_input: {cli_args.fuzzy_file_input.prompt()}")


def prompt_multiple_times(cli_args):
    log.result(f"name: {cli_args.name.prompt()}")
    log.result(f"name: {cli_args.name.prompt()}")
    log.result(f"name: {cli_args.name.prompt()}")
    log.result(f"name: {cli_args.name.prompt()}")


def default(cli_args):
    log.result(f"test: {cli_args.test.prompt()}")
    log.result(f"test: {cli_args.test.prompt()}")
    log.result(f"test: {cli_args.test.prompt()}")
    log.result(f"test: {cli_args.test.prompt()}")

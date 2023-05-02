from enum import Enum
from typing import Any, Optional, List

from pydantic import validator

from hexagon.domain.args import ToolArgs, OptionalArg, PositionalArg, Arg
from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.printer import log


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

    test: PositionalArg[str]
    name: OptionalArg[str] = Arg(None, prompt_message="input the person's name:")
    age: OptionalArg[int] = None
    country: OptionalArg[str] = "Argentina"
    likes: OptionalArg[list] = None
    tag: OptionalArg[Category] = Category.C
    available_tags: OptionalArg[List[Category]] = [Category.B, Category.E]
    total_amount: OptionalArg[float] = None

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
    if cli_args.test.value == "prompt_name_and_age":
        log.result(f"name: {cli_args.name.prompt()}")
        log.result(f"age: {cli_args.age.prompt()}")
        log.result(f"age type: {type(cli_args.age.value).__name__}")
    elif cli_args.test.value == "prompt_validate_age":
        log.result(f"age: {cli_args.age.prompt()}")
    elif cli_args.test.value == "prompt_show_default_value":
        log.result(f"country: {cli_args.country.prompt()}")
    elif cli_args.test.value == "prompt_list_value":
        log.result(f"likes: {cli_args.likes.prompt()}")
    elif cli_args.test.value == "prompt_enum_choices":
        log.result(f"tag: {cli_args.tag.prompt()}")
        log.result(f"tag type: {type(cli_args.tag.value).__name__}")
    elif cli_args.test.value == "prompt_list_enum_choices":
        log.result(f"available_tags: {cli_args.available_tags.prompt()}")
    elif cli_args.test.value == "prompt_validate_type":
        log.result(f"total_amount: {cli_args.total_amount.prompt()}")
        log.result(f"total_amount type: {type(cli_args.total_amount.value).__name__}")

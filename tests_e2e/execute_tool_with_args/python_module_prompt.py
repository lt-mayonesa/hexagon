from enum import Enum
from typing import Any, Optional, List

from pydantic import validator

from hexagon.domain.args import ToolArgs, OptionalArg, PositionalArg, Field
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
    name: OptionalArg[str] = Field(None, prompt_message="input the person's name:")
    age: OptionalArg[int] = None
    country: OptionalArg[str] = "Argentina"
    likes: OptionalArg[list] = None
    tag: OptionalArg[Category] = Category.C
    available_tags: OptionalArg[List[Category]] = [Category.B, Category.E]

    @validator("age")
    def validate_age(cls, value):
        if not value or int(value) < 18:
            raise ValueError("age must be greater than 18")
        return value

    @validator("age")
    def validate_age_max(cls, value):
        if not value or int(value) > 48:
            raise ValueError("age must be less than 48")
        return value


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    if cli_args.test == "prompt_name_and_age":
        log.result(f"name: {cli_args.prompt('name')}")
        log.result(f"age: {cli_args.prompt('age')}")
        log.result(f"age type: {type(cli_args.age).__name__}")
    elif cli_args.test == "prompt_validate_age":
        log.result(f"age: {cli_args.prompt('age')}")
    elif cli_args.test == "prompt_show_default_value":
        log.result(f"country: {cli_args.prompt('country')}")
    elif cli_args.test == "prompt_list_value":
        log.result(f"likes: {cli_args.prompt('likes')}")
    elif cli_args.test == "prompt_enum_choices":
        log.result(f"tag: {cli_args.prompt('tag')}")
        log.result(f"tag type: {type(cli_args.tag).__name__}")
    elif cli_args.test == "prompt_list_enum_choices":
        log.result(f"available_tags: {cli_args.prompt('available_tags')}")

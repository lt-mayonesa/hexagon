from enum import Enum
from typing import Any, Optional, List

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, Arg, PositionalArg
from hexagon.support.output.printer import log


class Scenario(Enum):
    arg_has_prompt_default = "arg_has_prompt_default"
    arg_has_default = "arg_has_default"
    enum_default = "enum_default"
    enum_multiselect = "enum_multiselect"


class Category(Enum):
    cat = "cat"
    dog = "dog"
    bird = "bird"
    insect = "insect"
    fish = "fish"


class Brand(Enum):
    ford = "ford"
    fiat = "fiat"
    toyota = "toyota"
    renault = "renault"


class Args(ToolArgs):
    scenario: PositionalArg[Scenario] = None
    name: PositionalArg[str] = Arg(None, prompt_default="John")
    age: PositionalArg[int] = Arg(23)
    category: PositionalArg[Category] = Arg(None, prompt_default=Category.insect)
    brands: PositionalArg[List[Brand]] = Arg(
        None, prompt_default=[Brand.toyota, Brand.renault]
    )


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    field = {
        Scenario.arg_has_prompt_default: cli_args.name,
        Scenario.arg_has_default: cli_args.age,
        Scenario.enum_default: cli_args.category,
        Scenario.enum_multiselect: cli_args.brands,
    }.get(cli_args.scenario.value)

    log.result(f"initial value: {field.value}")
    log.result(f"prompt result: {field.prompt()}")

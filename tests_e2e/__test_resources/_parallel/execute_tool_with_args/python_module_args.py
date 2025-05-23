from typing import Any, Optional

from pydantic import validator

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, PositionalArg, OptionalArg, Arg
from hexagon.support.output.printer import log


# noinspection PyMethodParameters
class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed and loaded automatically by hexagon
    """

    name: PositionalArg[str]
    age: PositionalArg[Optional[int]] = Arg(
        None, description="the person's age, if provided must be greater than 18"
    )
    nationality: PositionalArg[Optional[str]] = Arg("Argentinian")
    car_brand: OptionalArg[str] = Arg("Ford", description="the car's brand")
    car_model: OptionalArg[str] = Arg(None, description="the car's model")
    car_years: OptionalArg[list] = None

    @validator("nationality")
    def validate_nationality(cls, v):
        if v.value == "USA":
            raise ValueError("USA is not a valid nationality")
        return v

    @validator("car_brand")
    def validate_car_brand(cls, v):
        if v.value == "Chevrolet":
            raise ValueError("we don't accept Chevrolet cars")
        return v


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"name: {cli_args.name and cli_args.name.value}")
    log.result(f"age: {cli_args.age and cli_args.age.value}")
    log.result(f"nationality: {cli_args.nationality and cli_args.nationality.value}")
    log.result(f"car_brand: {cli_args.car_brand and cli_args.car_brand.value}")
    log.result(f"car_model: {cli_args.car_model and cli_args.car_model.value}")
    log.result(f"car_years: {cli_args.car_years and cli_args.car_years.value}")

from typing import Any, Optional

from pydantic import Field

from hexagon.domain.args import ToolArgs, PositionalArg, OptionalArg
from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.printer import log


class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed loaded automatically by hexagon
    """

    name: PositionalArg[str]
    age: PositionalArg[Optional[int]] = Field(
        None, description="the person's age, if provided must be greater than 18"
    )
    nationality: PositionalArg[Optional[str]] = "Argentinian"
    car_brand: OptionalArg[str] = Field("Ford", description="the car's brand")
    car_model: OptionalArg[str] = Field(None, description="the car's model")
    car_years: OptionalArg[list] = None


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    log.result(f"name: {cli_args.name}")
    log.result(f"age: {cli_args.age}")
    log.result(f"nationality: {cli_args.nationality}")
    log.result(f"car_brand: {cli_args.car_brand}")
    log.result(f"car_model: {cli_args.car_model}")
    log.result(f"car_years: {cli_args.car_years}")

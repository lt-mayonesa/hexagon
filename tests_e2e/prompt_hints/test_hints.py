from enum import Enum
from typing import Any, Optional, List

from pydantic import FilePath

from hexagon.domain.args import ToolArgs, OptionalArg, PositionalArg
from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.printer import log
from hexagon.support.prompt import prompt


class Category(str, Enum):
    A = "a"
    B = "b"
    C = "c"


class Test(Enum):
    HINTS_TEXT = "hints_text"
    HINTS_TEXT_MULTILINE = "hints_text_multiline"
    HINTS_SELECT = "hints_select"
    HINTS_CHECKBOX = "hints_checkbox"
    HINTS_CONFIRM = "hints_confirm"
    HINTS_FUZZY = "hints_fuzzy"
    HINTS_FUZZY_MULTISELECT = "hints_fuzzy_multiselect"
    HINTS_PATH = "hints_path"
    HINTS_NUMBER = "hints_number"


class Args(ToolArgs):
    """
    command line arguments for the tool
    they get parsed loaded automatically by hexagon
    """

    test: PositionalArg[Test] = None
    prompt_text: OptionalArg[str] = None
    prompt_text_multiline: OptionalArg[list] = None
    prompt_select: OptionalArg[Category] = Category.C
    prompt_checkbox: OptionalArg[List[Category]] = [Category.B, Category.A]
    prompt_fuzzy: OptionalArg[str] = None
    prompt_fuzzy_multiselect: OptionalArg[List[str]] = None
    prompt_path: OptionalArg[FilePath] = None


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    if cli_args.test.value == Test.HINTS_TEXT:
        log.result(f"result: {cli_args.prompt_text.prompt()}")
    elif cli_args.test.value == Test.HINTS_TEXT_MULTILINE:
        log.result(f"result: {cli_args.prompt_text_multiline.prompt()}")
    elif cli_args.test.value == Test.HINTS_SELECT:
        log.result(f"result: {cli_args.prompt_select.prompt()}")
    elif cli_args.test.value == Test.HINTS_CHECKBOX:
        log.result(f"result: {cli_args.prompt_checkbox.prompt()}")
    elif cli_args.test.value == Test.HINTS_CONFIRM:
        log.result(f"result: {prompt.confirm('Are you sure?', default=True)}")
    elif cli_args.test.value == Test.HINTS_FUZZY:
        fuzzy_prompt = cli_args.prompt_fuzzy.prompt(
            choices=["a", "b", "c", "d", "e", "f"]
        )
        log.result(f"result: {fuzzy_prompt}")
    elif cli_args.test.value == Test.HINTS_FUZZY_MULTISELECT:
        multiselect_prompt = cli_args.prompt_fuzzy_multiselect.prompt(
            choices=["a", "b", "c", "d", "e", "f"]
        )
        log.result(f"result: {multiselect_prompt}")
    elif cli_args.test.value == Test.HINTS_PATH:
        log.result(f"result: {cli_args.prompt_path.prompt()}")
    else:
        log.error(f"Unknown test: {cli_args.test.value}")

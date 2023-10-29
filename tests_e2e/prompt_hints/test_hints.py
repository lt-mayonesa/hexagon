from enum import Enum
from typing import Any, Optional, List

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg, PositionalArg, Arg
from hexagon.support.input.prompt import prompt
from hexagon.support.input.types import DirectoryPath, FilePath
from hexagon.support.output.printer import log


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
    HINTS_FILE_PATH = "hints_file_path"
    HINTS_DIRECTORY_PATH = "hints_directory_path"
    HINTS_NUMBER = "hints_number"
    HINTS_NUMBER_FLOAT = "hints_number_float"
    HINTS_SECRET = "hints_secret"


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
    prompt_fuzzy: OptionalArg[str] = Arg(
        None,
        searchable=True,
        choices=["a", "b", "c", "d", "e", "f"],
    )
    prompt_fuzzy_multiselect: OptionalArg[List[str]] = Arg(
        None,
        searchable=True,
        choices=["a", "b", "c", "d", "e", "f"],
    )
    prompt_file_path: OptionalArg[FilePath] = None
    prompt_directory_path: OptionalArg[DirectoryPath] = None
    prompt_number: OptionalArg[int] = None
    prompt_number_float: OptionalArg[float] = None
    prompt_text_secret: OptionalArg[str] = Arg(
        None,
        secret=True,
    )


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    scenarios = {
        Test.HINTS_TEXT: lambda: cli_args.prompt_text.prompt(),
        Test.HINTS_TEXT_MULTILINE: lambda: cli_args.prompt_text_multiline.prompt(),
        Test.HINTS_SELECT: lambda: cli_args.prompt_select.prompt().value,
        Test.HINTS_CHECKBOX: lambda: cli_args.prompt_checkbox.prompt(),
        Test.HINTS_CONFIRM: lambda: prompt.confirm("Are you sure?", default=True),
        Test.HINTS_FUZZY: lambda: cli_args.prompt_fuzzy.prompt(),
        Test.HINTS_FUZZY_MULTISELECT: lambda: cli_args.prompt_fuzzy_multiselect.prompt(),
        Test.HINTS_FILE_PATH: lambda: cli_args.prompt_file_path.prompt(),
        Test.HINTS_DIRECTORY_PATH: lambda: cli_args.prompt_directory_path.prompt(),
        Test.HINTS_NUMBER: lambda: cli_args.prompt_number.prompt(),
        Test.HINTS_NUMBER_FLOAT: lambda: cli_args.prompt_number_float.prompt(),
        Test.HINTS_SECRET: lambda: cli_args.prompt_text_secret.prompt(),
    }

    log.result(f"result: {scenarios[cli_args.test.value]()}")

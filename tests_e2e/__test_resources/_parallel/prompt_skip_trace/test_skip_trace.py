from enum import Enum
from typing import Any, Optional

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.support.input.args import ToolArgs, OptionalArg, PositionalArg


class Test(Enum):
    SKIP_TRACE_BOOL = "skip_trace_bool"
    SKIP_TRACE_BOOL_TWO_ARGS = "skip_trace_bool_two_args"
    SKIP_TRACE_CALLABLE = "skip_trace_callable"
    SKIP_TRACE_CALLABLE_FALSY = "skip_trace_callable_falsy"


class Args(ToolArgs):
    test: PositionalArg[Test] = None
    prompt_text: OptionalArg[str] = None
    prompt_text_two: OptionalArg[str] = None


def main(
    action: ActionTool,
    env: Optional[Env] = None,
    env_args: Any = None,
    cli_args: Args = None,
):
    scenarios = {
        Test.SKIP_TRACE_BOOL: skip_trace_bool,
        Test.SKIP_TRACE_BOOL_TWO_ARGS: skip_trace_bool_two_args,
        Test.SKIP_TRACE_CALLABLE: skip_trace_callable,
        Test.SKIP_TRACE_CALLABLE_FALSY: skip_trace_callable_falsy,
    }
    scenarios[cli_args.test.value](cli_args)


def skip_trace_bool(cli_args: Args):
    cli_args.prompt_text.prompt(skip_trace=True)


def skip_trace_bool_two_args(cli_args: Args):
    cli_args.prompt_text.prompt(skip_trace=True)
    cli_args.prompt_text_two.prompt()


def skip_trace_callable(cli_args: Args):
    cli_args.prompt_text.prompt(skip_trace=lambda x: x == "foo")


def skip_trace_callable_falsy(cli_args: Args):
    cli_args.prompt_text.prompt(skip_trace=lambda x: x == "bar")
    cli_args.prompt_text.prompt(skip_trace=lambda x: x == "bar")

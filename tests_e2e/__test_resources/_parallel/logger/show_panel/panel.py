from enum import Enum

from hexagon.support.input.args import ToolArgs, PositionalArg
from hexagon.support.output.printer import log


class Test(Enum):
    DEFAULT_ARGS_PANEL = "default_args_panel"
    TITLE_AND_FOOTER = "title_and_footer"
    FIT_FALSE = "fit_false"
    PADDING_AND_JUSTIFY = "padding_and_justify"


class Args(ToolArgs):
    test: PositionalArg[Test] = None


def main(_, __, ___, cli_args: Args):
    if cli_args.test.value == Test.DEFAULT_ARGS_PANEL:
        log.panel("This is a panel")
    elif cli_args.test.value == Test.TITLE_AND_FOOTER:
        log.panel("This is a panel", title="title", footer="footer")
    elif cli_args.test.value == Test.FIT_FALSE:
        log.panel("This is a panel", title="title", fit=False)
    elif cli_args.test.value == Test.PADDING_AND_JUSTIFY:
        log.panel(
            "This is a panel\n" "The content will be justified to the center",
            padding=(4, 2),
            justify="center",
        )

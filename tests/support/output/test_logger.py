import pytest
from rich.syntax import Syntax

from hexagon.support.output.printer import Logger
from hexagon.support.output.printer.themes import LoggingTheme


class Console:
    def __init__(self) -> None:
        super().__init__()
        self.__output = []

    def print(self, value):
        self.__output.append(value)

    @property
    def output(self):
        return "\n".join(self.__output)

    @property
    def raw_output(self):
        return self.__output


@pytest.mark.parametrize(
    "decoration,message,expected",
    [
        ("", "", ""),
        ("╭╼ ", "docker", "╭╼ docker"),
        ("╭╼            ", "sarasa asdfasd ", "╭╼            sarasa asdfasd "),
    ],
)
def test_log_start(decoration, message, expected):
    console = Console()

    Logger(LoggingTheme(start=decoration), console).start(message)

    assert console.output == expected


@pytest.mark.parametrize(
    "border,repeat,expected",
    [
        ("", 1, ""),
        ("│", 1, "│"),
        ("│", 0, ""),
        ("border", 5, "\n".join(["border", "border", "border", "border", "border"])),
        ("│         ", 1, "│         "),
    ],
)
def test_log_gap(border, repeat, expected):
    console = Console()

    Logger(LoggingTheme(border=border), console).gap(repeat)

    assert console.output == expected


@pytest.mark.parametrize(
    "decoration,message,gap_start,gap_end,expected",
    [
        ("", "hello", 0, 0, "hello"),
        ("│", "hello", 0, 0, "│hello"),
        ("│ ", "hello", 0, 0, "│ hello"),
        ("│ ", "hello", 1, 1, "│ \n│ hello\n│ "),
        ("│ ", "hello", 5, 1, "│ \n│ \n│ \n│ \n│ \n│ hello\n│ "),
    ],
)
def test_log_info(decoration, message, gap_start, gap_end, expected):
    console = Console()

    Logger(LoggingTheme(border=decoration), console).info(
        message, gap_start=gap_start, gap_end=gap_end
    )

    assert console.output == expected


@pytest.mark.parametrize(
    "decoration,message,gap_start,gap_end,expected",
    [
        ("│ ", ("hello", "world"), 0, 0, "│ hello\n│ world"),
        ("│ ", ("hello", "world"), 2, 3, "│ \n│ \n│ hello\n│ world\n│ \n│ \n│ "),
        ("│ ", ("hello", ""), 0, 0, "│ hello\n│ "),
        (
            "│ ",
            ("hello", "world", "how", "are", "you"),
            0,
            0,
            "│ hello\n│ world\n│ how\n│ are\n│ you",
        ),
    ],
)
def test_log_info_with_multiple_message(
    decoration, message, gap_start, gap_end, expected
):
    console = Console()

    Logger(LoggingTheme(border=decoration), console).info(
        *message, gap_start=gap_start, gap_end=gap_end
    )

    assert console.output == expected


@pytest.mark.parametrize(
    "decoration,message,expected",
    [
        ("", "", ""),
        ("├ ", "docker", "├ docker"),
        ("├            ", "sarasa asdfasd ", "├            sarasa asdfasd "),
    ],
)
def test_log_result(decoration, message, expected):
    console = Console()

    Logger(LoggingTheme(border_result=decoration), console).result(message)

    assert console.output == expected


@pytest.mark.parametrize(
    "process_out,process_in,message,expected",
    [
        ("", "", "", "\n\n\n\n"),
        ("┆", "┆", "docker", "┆\n\ndocker\n\n┆"),
        ("┆", "", "sarasa asdfasd ", "┆\n\nsarasa asdfasd \n\n"),
    ],
)
def test_log_example(process_out, process_in, message, expected):
    console = Console()

    Logger(
        LoggingTheme(process_out=process_out, process_in=process_in), console
    ).example(message)

    assert console.output == expected


def test_log_example_with_syntax():
    console = Console()

    Logger(LoggingTheme(), console).example(
        "# this is a yaml file\nkey: value",
        syntax="yaml",
        show_line_numbers=True,
        decorator_start=False,
        decorator_end=False,
    )

    assert isinstance(console.raw_output[0], Syntax)
    assert console.raw_output[0].code == "# this is a yaml file\nkey: value"
    assert console.raw_output[0].lexer.name == "YAML"
    assert console.raw_output[0].line_numbers is True
    assert console.raw_output[0].line_range is None


def test_log_file():
    console = Console()

    Logger(LoggingTheme(), console).file(__file__, line_range=(1, 10))

    assert isinstance(console.raw_output[0], Syntax)
    assert console.raw_output[0].code == open(__file__, "r").read()
    assert console.raw_output[0].lexer.name == "Python"
    assert console.raw_output[0].line_numbers is True
    assert console.raw_output[0].line_range == (1, 10)


def test_panel_color():
    console = Console()

    Logger(LoggingTheme(), console).panel("my panel", color="red")

    assert console.raw_output[0].style == "red"
    assert console.raw_output[0].renderable.style == "red"
    assert console.raw_output[0].renderable.markup == "[red]my panel[/red]"

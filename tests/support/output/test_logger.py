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
def test_log_start_formats_message_with_decoration_prefix(
    decoration, message, expected
):
    """
    Given a Logger with a specific start decoration in its theme.
    When the start() method is called with a message.
    Then the console output should be the decoration followed by the message.
    """
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
def test_log_gap_repeats_border_character_the_specified_number_of_times(
    border, repeat, expected
):
    """
    Given a Logger with a specific border character in its theme.
    When the gap() method is called with a specific repeat count.
    Then the console output should contain the border character repeated the specified number of times.
    """
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
def test_log_info_formats_message_with_decoration_and_optional_gaps(
    decoration, message, gap_start, gap_end, expected
):
    """
    Given a Logger with a specific border decoration in its theme.
    When the info() method is called with a message and gap_start/gap_end parameters.
    Then the console output should include the message with the decoration prefix.
    And the specified number of empty decorated lines before and after the message.
    """
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
def test_log_info_formats_multiple_messages_with_decoration_and_optional_gaps(
    decoration, message, gap_start, gap_end, expected
):
    """
    Given a Logger with a specific border decoration in its theme.
    When the info() method is called with multiple messages and gap_start/gap_end parameters.
    Then the console output should include each message on a separate line with the decoration prefix.
    And the specified number of empty decorated lines before and after the messages.
    """
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
def test_log_result_formats_message_with_result_decoration_prefix(
    decoration, message, expected
):
    """
    Given a Logger with a specific border_result decoration in its theme.
    When the result() method is called with a message.
    Then the console output should be the result decoration followed by the message.
    """
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
def test_log_example_formats_message_with_process_decorators(
    process_out, process_in, message, expected
):
    """
    Given a Logger with specific process_out and process_in decorations in its theme.
    When the example() method is called with a message.
    Then the console output should include the message surrounded by the process decorators.
    And have appropriate spacing between the decorators and the message.
    """
    console = Console()

    Logger(
        LoggingTheme(process_out=process_out, process_in=process_in), console
    ).example(message)

    assert console.output == expected


def test_log_example_with_syntax_creates_rich_syntax_object_with_specified_parameters():
    """
    Given a Logger instance
    When the example() method is called with syntax='yaml', show_line_numbers=True, and decorator flags set to False.
    Then a rich.syntax.Syntax object should be created with the specified code.
    And the Syntax object should have the YAML lexer, line numbers enabled, and no line range restriction.
    """
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


def test_log_file_creates_syntax_object_with_file_contents_and_line_range():
    """
    Given a Logger instance
    When the file() method is called with a file path and line_range=(1, 10).
    Then a rich.syntax.Syntax object should be created with the file's contents.
    And the Syntax object should have the Python lexer, line numbers enabled, and line range set to (1, 10).
    """
    console = Console()

    Logger(LoggingTheme(), console).file(__file__, line_range=(1, 10))

    assert isinstance(console.raw_output[0], Syntax)
    assert console.raw_output[0].code == open(__file__, "r").read()
    assert console.raw_output[0].lexer.name == "Python"
    assert console.raw_output[0].line_numbers is True
    assert console.raw_output[0].line_range == (1, 10)


def test_panel_applies_specified_color_to_panel_and_its_content():
    """
    Given a Logger instance
    When the panel() method is called with a message and color='red'.
    Then the panel should have its style set to 'red'.
    And the panel's renderable should have its style set to 'red'.
    And the panel's renderable markup should wrap the message in red color tags.
    """
    console = Console()

    Logger(LoggingTheme(), console).panel("my panel", color="red")

    assert console.raw_output[0].style == "red"
    assert console.raw_output[0].renderable.style == "red"
    assert console.raw_output[0].renderable.markup == "[red]my panel[/red]"

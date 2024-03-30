from types import TracebackType
from typing import Optional, Union, Type, Literal

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from hexagon.support.output.printer.themes import load_theme, LoggingTheme


class Logger:
    def __init__(
        self, theme: Union[str, LoggingTheme], console: Console = None
    ) -> None:
        self.__console = None
        self.__decorations = None
        self.__live_status = None
        if isinstance(theme, str):
            self.load_theme(theme)
        else:
            self.load_theme(theme, console)

    def start(self, message: str):
        """
        Print a start message to the console.

        Usually used at the beginning of the CLI invocation.
        ie:
        ╭╼ My CLI

        :param message: the message to be printed
        """
        if not self.__decorations.result_only:
            self.__console.print(f"{self.__decorations.start}{message}")

    def gap(self, repeat: int = 1):
        """
        Print a gap to the console.

        ie:
        log.gap(2)
        log.info("some output")

        result:
        │
        │
        │ some output

        :param repeat: the number of times the gap should be printed
        """
        if not self.__decorations.result_only:
            for _ in range(repeat):
                self.__console.print(self.__decorations.border)

    def info(self, *message: str, gap_start: int = 0, gap_end: int = 0):
        """
        Print an informatory message to the console.
        This the most common type of message to be printed.

        ie:
        log.info("some output")

        result:
        │ some output

        :param message: the message to be printed
        :param gap_start: the number of gaps to be printed before the message
        :param gap_end: the number of gaps to be printed after the message
        """
        if not self.__decorations.result_only:
            self.gap(gap_start)
            for msg in message:
                self.__console.print(f"{self.__decorations.border}{msg}")
            self.gap(gap_end)

    def result(self, message: str):
        """
        Print a result message to the console.
        Result messages are usually the output of a command.

        ie:
        log.result("some output")

        result:
        ├ some output

        :param message: the message to be printed
        """
        self.__console.print(f"{self.__decorations.border_result}{message}")

    def example(
        self,
        message: Union[str, Syntax],
        syntax: Optional[str] = None,
        show_line_numbers: bool = False,
        line_range: Optional[tuple] = None,
        decorator_start: Union[str, bool] = True,
        decorator_end: Union[str, bool] = True,
        **kwargs,
    ):
        """
        Print an example to the console.
        Examples are usually code snippets, file contents, shell commands,
        basically anything that should be an example to the user.

        ie:
        log.info("running command")
        log.example("$ docker run -it ubuntu:latest")

        result:
        │ running command
        ┆

        $ docker run -it ubuntu:latest

        ┆

        :param message: the message to be printed
        :param syntax: the syntax highlighting to be used
        :param show_line_numbers: whether to show line numbers
        :param line_range: range of lines to be printed
        :param decorator_start: the decorator to be printed before the message
        :param decorator_end: the decorator to be printed after the message
        :param kwargs: additional arguments to be passed to the Syntax object
        """

        def __use_decorator(param, default):
            return param if isinstance(param, str) else default

        if not self.__decorations.result_only and decorator_start is not False:
            self.__console.print(
                __use_decorator(decorator_start, f"{self.__decorations.process_out}\n")
            )

        if not isinstance(message, Syntax) and syntax:
            message = Syntax(
                message,
                lexer=syntax,
                line_numbers=show_line_numbers,
                line_range=line_range,
                **kwargs,
            )

        self.__console.print(message)

        if not self.__decorations.result_only and decorator_end is not False:
            self.__console.print(
                __use_decorator(decorator_end, f"\n{self.__decorations.process_in}")
            )

    def file(
        self,
        path: str,
        encoding: str = "utf-8",
        syntax: Optional[str] = None,
        show_line_numbers: bool = True,
        line_range: Optional[tuple] = None,
        **kwargs,
    ):
        """
        Pretty print a file from the specified path to the console.
        The syntax highlighting will be inferred from the file extension.

        :param path: Path to the file to be printed
        :param encoding: Encoding of the file
        :param syntax: Syntax to be used for highlighting, defaults to inferred
        :param show_line_numbers: Whether to show line numbers
        :param line_range: Range of lines to be printed
        :param kwargs: Additional arguments to be passed to the Syntax object
        """
        self.__console.print(
            Syntax.from_path(
                path,
                encoding=encoding,
                lexer=syntax,
                line_numbers=show_line_numbers,
                line_range=line_range,
                **kwargs,
            )
        )

    def panel(
        self,
        message,
        title: str = None,
        footer: str = None,
        color: str = None,
        fit: bool = True,
        padding: tuple = None,
        justify: Literal["default", "left", "center", "right", "full"] = None,
        **kwargs,
    ):
        """
        Print a panel to the console.
        A panel is a block of text that is highlighted.

        ie:
        log.panel("No hexagon bins path configured yet.")

        result:
        ╭──────────────────────────────────────────────╮
        │                                              │
        │     No hexagon bins path configured yet.     │
        │                                              │
        ╰──────────────────────────────────────────────╯

        :param message: the message to be printed inside the panel
        :param title: the title of the panel
        :param footer: the footer of the panel
        :param color: the color of the panel borders and text
        :param fit: whether the panel should fit the content or not
        :param padding: the padding of the panel
        :param justify: the justification of the text inside the panel
        :param kwargs: additional arguments to be passed to the Panel object
        """
        color = color or "yellow"
        self.extra(
            Panel(
                Text.from_markup(message, justify=justify, style=color),
                style=color,
                padding=padding or (1, 5),
                title=title,
                subtitle=footer,
                expand=not fit,
                **kwargs,
            )
        )

    def error(self, message: str, err: Optional[Exception] = None):
        """
        Print a red error message to the console.
        Error messages are usually used to display errors to the user.

        ie:
        log.error("an error occurred")

        result:
        [red]an error occurred

        :param message: the message to be printed
        :param err: the exception to be printed, if any
        """
        self.__console.print(f"[red]{message}")
        if err:
            self.__console.print(err)

    def extra(self, *message: Union[str, Panel]):
        """
        Useful for printing additional information to the console.

        ie:
        log.extra("To run this tool again do:")
        log.extra("     hexagon install")

        result:
        To run this tool again do:
             hexagon install

        :param message: the messages to be printed
        """
        if not self.__decorations.result_only:
            for msg in message:
                self.__console.print(msg)

    def finish(self, message: str = None):
        """
        Print a closing message to the console.
        Usually used at the end of the CLI invocation.

        ie:
        log.finish("done")

        result:
        ╰╼ done

        :param message: the message to be printed
        """
        if not self.__decorations.result_only:
            self.__console.print(f"{self.__decorations.finish}{message or ''}")

    def status(self, message: str = None):
        """
        Show a progress status icon to the user.
        Useful for long-running commands.

        ie:
        with log.status("running command"):
            # command execution
            pass

        result:
        ⠧ running command

        :param message: the message to be shown alongside the status icon
        """
        if self.__live_status:
            self.__live_status.update(message)
        else:
            self.__live_status = NestableStatus(self.__console.status(message))
        return self.__live_status

    def load_theme(self, theme: Union[str, LoggingTheme], console: Console = None):
        self.__decorations = (
            theme if isinstance(theme, LoggingTheme) else load_theme(theme)
        )
        self.__console = console or Console(
            color_system="auto" if self.__decorations.show_colors else None
        )

    def use_borders(self):
        return self.__decorations.prompt_border

    def status_aware(self, decorated):
        """
        Decorator that stops the status bar while the decorated function is running.

        :param decorated: the function to be decorated
        :return: the decorated function
        """

        def decorator(cls, *args, **kwargs):
            stopped = False
            if self.__live_status and self.__live_status.active:
                self.__live_status.stop()
                stopped = True

            res = decorated(*args, **kwargs)

            if stopped:
                self.__live_status.start()
            return res

        return decorator


class NestableStatus:
    """
    A wrapper for rich's Status class that allows nesting status calls.

    ie.:
    with log.status("foo"):
        # status should show "foo"
        with log.status("bar"):
            # status should show "bar"
        # status should show "foo"
    # status should be hidden

    """

    def __init__(self, status):
        self.__status = status
        self.__levels = 1

    @property
    def renderable(self):
        return self.__status.renderable

    @property
    def console(self):
        return self.__status.console

    def update(self, *args, **kwargs):
        self.__levels += 1
        self.__status.update(*args, **kwargs)

    def start(self):
        self.__status.start()

    def stop(self) -> None:
        self.__status.stop()

    def __rich__(self):
        return self.__status.__rich__()

    def __enter__(self):
        self.__status.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        self.__levels -= 1
        if self.__levels <= 1:
            self.__status.__exit__(exc_type, exc_val, exc_tb)

    @property
    def active(self):
        return self.__levels > 1

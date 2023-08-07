from types import TracebackType
from typing import Optional, Union, Type

from rich.console import Console
from rich.syntax import Syntax

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
        if not self.__decorations.result_only:
            self.__console.print(f"{self.__decorations.start}{message}")

    def gap(self, repeat: int = 1):
        if not self.__decorations.result_only:
            for _ in range(repeat):
                self.__console.print(self.__decorations.border)

    def info(self, *message: str, gap_start: int = 0, gap_end: int = 0):
        if not self.__decorations.result_only:
            self.gap(gap_start)
            for msg in message:
                self.__console.print(f"{self.__decorations.border}{msg}")
            self.gap(gap_end)

    def result(self, message: str):
        self.__console.print(f"{self.__decorations.border_result}{message}")

    def example(
        self,
        *message: Union[str, Syntax],
        decorator_start: Union[str, bool] = True,
        decorator_end: Union[str, bool] = True,
    ):
        def __use_decorator(param, default):
            return param if isinstance(param, str) else default

        if not self.__decorations.result_only and decorator_start is not False:
            self.__console.print(
                __use_decorator(decorator_start, f"{self.__decorations.process_out}\n")
            )

        for msg in message:
            self.__console.print(msg)

        if not self.__decorations.result_only and decorator_end is not False:
            self.__console.print(
                __use_decorator(decorator_end, f"\n{self.__decorations.process_in}")
            )

    def error(self, message: str, err: Optional[Exception] = None):
        self.__console.print(f"[red]{message}")
        if err:
            self.__console.print(err)

    def extra(self, *message: str):
        if not self.__decorations.result_only:
            for msg in message:
                self.__console.print(msg)

    def finish(self, message: str = None):
        if not self.__decorations.result_only:
            self.__console.print(f"{self.__decorations.finish}{message or ''}")

    def status(self, message: str = None):
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

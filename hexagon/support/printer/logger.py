from typing import Optional, Union

from rich.console import Console
from rich.syntax import Syntax

from hexagon.support.printer.themes import LoggingTheme


class Logger:
    def __init__(self, console: Console, decorations: LoggingTheme) -> None:
        self.__console = console
        self.__decorations = decorations

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

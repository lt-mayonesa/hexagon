from typing import List, Callable


class HexagonError(Exception):
    """Base class for all Hexagon errors."""

    def __init__(self, error_printer: Callable, exit_status: int = 1) -> None:
        super().__init__("hexagon error")
        self.exit_status = exit_status
        self.error_printer = error_printer

    def print_error(self, logger):
        self.error_printer(logger)


class ListHexagonError(HexagonError):
    """A list of errors."""

    def __init__(self, errors: List[str]) -> None:
        self.errors = errors
        super().__init__(self._error_printer)

    def _error_printer(self, logger) -> None:
        for error in self.errors:
            logger.error(error)


class SilentHexagonError(HexagonError):
    """A silent error."""

    def __init__(self) -> None:
        super().__init__(lambda x: None)

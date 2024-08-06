from hexagon.domain.hexagon_error import HexagonError


class MultipleHintsNotSupportedError(HexagonError):
    def __init__(self, types: tuple) -> None:
        self.message = f"Multiple hints not supported: {types}"
        super().__init__(self._error_printer)

    def _error_printer(self, logger):
        logger.error(self.message)

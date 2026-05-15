from typing import List, Optional

from hexagon.domain.hexagon_error import HexagonError


class AgentModeBlockedError(HexagonError):
    """
    Raised when a prompt is triggered while agent mode is active.

    In agent mode all interactive prompts are disabled. Agents are expected to
    supply every required argument up-front via CLI flags. This error reports
    which argument is missing and, when applicable, the set of accepted values
    or the expected type so the agent can retry with a complete invocation.
    """

    def __init__(  # noqa: B042
        self,  # noqa: B042
        name: str,  # noqa: B042
        possible_values: Optional[List] = None,  # noqa: B042
        expected_type: Optional[str] = None,  # noqa: B042
    ) -> None:  # noqa: B042
        self.name = name
        self.possible_values = possible_values
        self.expected_type = expected_type
        super().__init__(self._error_printer)

    def _error_printer(self, logger) -> None:
        logger.error(
            f"Agent mode is active: '{self.name}' requires a value but prompt is disabled."
        )
        if self.possible_values is not None:
            logger.error(
                f"Possible values: {', '.join(str(v) for v in self.possible_values)}"
            )
        elif self.expected_type is not None:
            logger.error(f"Expected type: {self.expected_type}")

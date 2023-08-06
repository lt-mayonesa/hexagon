import os
import sys
import traceback
from pathlib import Path
from typing import Optional

from pydantic import ValidationError
from rich import traceback as rich_traceback

from hexagon.domain.hexagon_error import ListHexagonError, HexagonError
from hexagon.support.output.printer import Logger


class ToolExecutionError(ListHexagonError):
    def __init__(
        self, return_code, executed_command, executable_str, custom_tools_path
    ) -> None:
        errors = [
            _("error.support.execute.errors.command_result_code").format(
                executed_command=executed_command, return_code=return_code
            )
        ]

        if return_code == 127:
            errors.append(
                _("error.support.execute.errors.could_not_execute").format(
                    action=executable_str
                )
            )
            errors.append(_("error.support.execute.errors.we_tried"))
            errors.append(
                _("error.support.execute.errors.attempt_cli_custom_dir").format(
                    path=custom_tools_path
                )
            )
            errors.append(
                _("error.support.execute.errors.attempt_internal_tools").format(
                    package="hexagon.actions.external"
                )
            )
            errors.append(
                _("error.support.execute.errors.attempt_known_script").format(
                    extensions=".js, .sh"
                )
            )
            errors.append(_("error.support.execute.errors.attempt_inline_command"))
        super().__init__(errors)


class ActionInputError(ListHexagonError):
    def __init__(self, e: ValidationError, tool_name: str) -> None:
        errors = [
            _("error.support.execute.errors.invalid_input").format(
                count=len(e.errors()), tool=tool_name
            )
        ]
        for error in e.errors():
            errors.append(
                os.linesep
                + _("error.support.execute.errors.invalid_argument").format(
                    loc=error["loc"][0], message=error["msg"]
                )
            )
        super().__init__(errors)


class WithTracebackError(HexagonError):
    def __init__(self, action_id: str, custom_tools_path: Optional[str] = None) -> None:
        tb, execution = self.__pretty_print_external_error(action_id, custom_tools_path)
        self.traceback = tb
        self.execution = execution
        self.error = None
        super().__init__(self._error_printer)

    def _error_printer(self, logger: Logger):
        if self.traceback:
            logger.example(self.traceback, decorator_start=False, decorator_end=False)
        else:
            logger.error(self.execution)

        logger.error(self.error)

    @classmethod
    def __pretty_print_external_error(
        cls, action_id: str, custom_tools_path: Optional[str]
    ) -> (str, str):
        exc_type, exc_value, tb = sys.exc_info()

        trace = (
            cls.__find_python_module_in_traceback(action_id, tb, custom_tools_path)
            if custom_tools_path
            else tb
        )

        return (
            rich_traceback.Traceback.from_exception(exc_type, exc_value, trace),
            exc_value,
        )

    @classmethod
    def __find_python_module_in_traceback(
        cls, action_id: str, tb, custom_tools_path: str
    ):
        return next(
            (
                t
                for t, path, file_name in cls.__walk_tb(tb)
                if file_name == action_id
                or path == os.path.join(custom_tools_path, action_id)
            ),
            None,
        )

    @classmethod
    def __walk_tb(cls, tb):
        def extract_metadata(_t):
            try:
                p = Path(traceback.extract_tb(_t)[0].filename)
                return p.parent, p.stem
            except IndexError:
                return None

        while tb is not None:
            path, file_name = extract_metadata(tb)
            yield tb, path.__str__(), file_name
            tb = tb.tb_next


class ActionImportError(WithTracebackError):
    def __init__(self, action_id, custom_tools_path) -> None:
        super().__init__(action_id, custom_tools_path)
        self.error = _("error.support.execute.errors.python_dependency_error")


class ActionExecuteError(WithTracebackError):
    def __init__(self, action_id, custom_tools_path) -> None:
        super().__init__(action_id, custom_tools_path)
        self.error = _("error.support.execute.errors.execute_tool_failed").format(
            action=action_id
        )

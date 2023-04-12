import inspect
import time
from functools import wraps
from subprocess import Popen
from typing import Callable, Dict, List, Optional, Union

from tests_e2e.__specs.utils.assertions import (
    Expected_Process_Output,
    assert_process_output,
    assert_process_ended,
)
from tests_e2e.__specs.utils.cli import (
    ARROW_DOWN_CHARACTER,
    ARROW_UP_CHARACTER,
    LINE_FEED_CHARACTER,
    ESCAPE_CHARACTER,
    CARRIAGE_RETURN_CHARACTER,
    BACKSPACE_CHARACTER,
    CONTROL_C_CHARACTER,
    SPACE_BAR_CHARACTER,
)
from tests_e2e.__specs.utils.config import write_hexagon_config
from tests_e2e.__specs.utils.run import (
    run_hexagon_e2e_test,
    write_to_process,
    clean_hexagon_environment,
)


def log(func):
    """
    Decorator to print function call details.

    This includes parameters names and effective values.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str = ", ".join(
            map(
                "{0[0]} = {0[1]!r}".format,
                {k: v for k, v in func_args.items() if k != "self"}.items(),
            )
        )
        print(f"step -> {func.__name__} ( {func_args_str} )")
        return func(*args, **kwargs)

    return wrapper


class HexagonSpec:
    HEXAGON_TEST_SHELL = "HEXAGON_TEST_SHELL"
    HEXAGON_THEME = "HEXAGON_THEME"
    HEXAGON_UPDATE_DISABLED = "HEXAGON_UPDATE_DISABLED"
    HEXAGON_CLI_UPDATE_DISABLED = "HEXAGON_CLI_UPDATE_DISABLED"
    HEXAGON_DISABLE_SPINNER = "HEXAGON_DISABLE_SPINNER"
    HEXAGON_SEND_TELEMETRY = "HEXAGON_SEND_TELEMETRY"
    HEXAGON_STORAGE_PATH = "HEXAGON_STORAGE_PATH"
    HEXAGON_CONFIG_FILE = "HEXAGON_CONFIG_FILE"

    def __init__(self, file) -> None:
        self.__file = file
        self.process: Optional[Popen[str]] = None
        self.command = None
        self.lines_read: List[str] = []
        self.last_input = None

    @log
    def given_a_cli_yaml(self, config: dict):
        write_hexagon_config(self.__file, config)
        return self

    @log
    def run_hexagon(
        self,
        command: List[str] = None,
        os_env_vars: Optional[Dict[str, str]] = None,
        test_file_path_is_absolute: bool = False,
        cwd: str = None,
    ):
        __tracebackhide__ = True
        if command:
            self.command = command
            self.process = run_hexagon_e2e_test(
                self.__file,
                self.command,
                os_env_vars=os_env_vars,
                test_file_path_is_absoulte=test_file_path_is_absolute,
                cwd=cwd,
            )
        else:
            self.process = run_hexagon_e2e_test(
                self.__file,
                os_env_vars=os_env_vars,
                test_file_path_is_absoulte=test_file_path_is_absolute,
                cwd=cwd,
            )
        return self

    @log
    def with_shared_behavior(self, func: Callable):
        __tracebackhide__ = True
        func(self)
        return self

    @log
    def then_output_should_be(
        self,
        expected_output: List[Expected_Process_Output],
        discard_until_first_match=False,
    ):
        __tracebackhide__ = True
        lines_read = assert_process_output(
            self.process,
            expected_output,
            discard_until_first_match=discard_until_first_match,
        )
        self.lines_read.extend(lines_read)
        return self

    @log
    def then_output_should_not_contain(
        self,
        output_to_match: List[Expected_Process_Output],
    ):
        __tracebackhide__ = True
        # noinspection PyBroadException
        try:
            self.then_output_should_be(output_to_match, discard_until_first_match=True)
            matched = True
        except Exception:
            matched = False

        if matched:
            raise Exception(f"Output contains expected content:\n{output_to_match}")

        return self

    @log
    def arrow_down(self):
        __tracebackhide__ = True
        write_to_process(self.process, ARROW_DOWN_CHARACTER)
        return self

    @log
    def arrow_up(self):
        __tracebackhide__ = True
        write_to_process(self.process, ARROW_UP_CHARACTER)
        return self

    @log
    def enter(self):
        __tracebackhide__ = True
        return self.write(LINE_FEED_CHARACTER)

    @log
    def space_bar(self):
        __tracebackhide__ = True
        return self.write(SPACE_BAR_CHARACTER)

    @log
    def esc(self):
        __tracebackhide__ = True
        return self.write(ESCAPE_CHARACTER)

    @log
    def carriage_return(self):
        __tracebackhide__ = True
        return self.write(CARRIAGE_RETURN_CHARACTER)

    @log
    def input(self, text: str):
        __tracebackhide__ = True
        self.last_input = text
        return self.write(f"{text}{LINE_FEED_CHARACTER}")

    @log
    def erase(self, val: Optional[Union[str, int]] = None):
        __tracebackhide__ = True
        if not val and self.last_input:
            for _ in self.last_input:
                self.write(BACKSPACE_CHARACTER)
            self.last_input = None
        elif isinstance(val, int):
            for _ in range(val):
                self.write(BACKSPACE_CHARACTER)
        else:
            for _ in val:
                self.write(BACKSPACE_CHARACTER)
        return self

    def write(self, text: str):
        __tracebackhide__ = True
        write_to_process(self.process, text)
        return self

    @log
    def exit(self, status: int = 0, timeout_in_seconds: int = 5):
        __tracebackhide__ = True
        assert_process_ended(
            self.process,
            exit_status=status,
            timeout_in_seconds=timeout_in_seconds,
            lines_read=self.lines_read,
        )
        clean_hexagon_environment()
        return self

    @log
    def force_exit(self):
        return self.write(CONTROL_C_CHARACTER)

    def wait(self, seconds: int):
        time.sleep(seconds)
        return self

    @property
    def _and_(self):
        return self


def as_a_user(test_file):
    return HexagonSpec(test_file)

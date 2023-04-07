import time
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

    def given_a_cli_yaml(self, config: dict):
        write_hexagon_config(self.__file, config)
        return self

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

    def with_shared_behavior(self, func: Callable):
        __tracebackhide__ = True
        func(self)
        return self

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

    def arrow_down(self):
        __tracebackhide__ = True
        write_to_process(self.process, ARROW_DOWN_CHARACTER)
        return self

    def arrow_up(self):
        __tracebackhide__ = True
        write_to_process(self.process, ARROW_UP_CHARACTER)
        return self

    def enter(self):
        __tracebackhide__ = True
        return self.write(LINE_FEED_CHARACTER)

    def space_bar(self):
        __tracebackhide__ = True
        return self.write(SPACE_BAR_CHARACTER)

    def esc(self):
        __tracebackhide__ = True
        return self.write(ESCAPE_CHARACTER)

    def carriage_return(self):
        __tracebackhide__ = True
        return self.write(CARRIAGE_RETURN_CHARACTER)

    def input(self, text: str):
        __tracebackhide__ = True
        return self.write(f"{text}{LINE_FEED_CHARACTER}")

    def erase(self, val: Union[str, int]):
        __tracebackhide__ = True
        if isinstance(val, int):
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

    @property
    def _and_(self):
        return self

    def force_exit(self):
        return self.write(CONTROL_C_CHARACTER)

    def wait(self, seconds: int):
        time.sleep(seconds)
        return self


def as_a_user(test_file):
    return HexagonSpec(test_file)

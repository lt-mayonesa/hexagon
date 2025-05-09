import inspect
import time
from subprocess import Popen
from typing import Callable, Dict, List, Optional, Union

from tests_e2e.__specs.utils.assertions import (
    Expected_Process_Output,
    assert_process_output,
    assert_process_ended,
    assert_execution_time,
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
    TAB_CHARACTER,
)
from tests_e2e.__specs.utils.config import write_hexagon_config
from tests_e2e.__specs.utils.console import print
from tests_e2e.__specs.utils.run import (
    run_hexagon_e2e_test,
    write_to_process,
    clean_hexagon_environment,
    init_hexagon_e2e_test,
)


def _log(f, *args, **kwargs):
    """
    Prints the hexagon step being executed.

    This was previously defined as a decorator, using ParamSpec to support type hints.
    But it wasn't working correctly as decorated methods are part of a class. :shrug:

    :param f: reference to the function being logged
    :param args: function args
    :param kwargs: function kwargs
    :return: None
    """
    func_args = inspect.signature(f).bind(*args, **kwargs).arguments
    func_args_str = map(
        "{0[0]} = {0[1]!r}".format,
        {k: v for k, v in func_args.items() if k != "self"}.items(),
    )
    print(f"[dim]step -> [/dim]{f.__name__} {'()' if not func_args else '('}")
    for arg in func_args_str:
        print(f"\t[dim]{arg}")
    if func_args:
        print(")")


class HexagonSpec:
    HEXAGON_TEST_SHELL = "HEXAGON_TEST_SHELL"
    HEXAGON_THEME = "HEXAGON_THEME"
    HEXAGON_UPDATE_DISABLED = "HEXAGON_UPDATE_DISABLED"
    HEXAGON_CLI_UPDATE_DISABLED = "HEXAGON_CLI_UPDATE_DISABLED"
    HEXAGON_SEND_TELEMETRY = "HEXAGON_SEND_TELEMETRY"
    HEXAGON_STORAGE_PATH = "HEXAGON_STORAGE_PATH"
    HEXAGON_CONFIG_FILE = "HEXAGON_CONFIG_FILE"

    def __init__(self, file, test_dir=None) -> None:
        self.__file = file
        self.test_dir = init_hexagon_e2e_test(self.__file, test_dir)
        self.process: Optional[Popen[str]] = None
        self.command = None
        self.lines_read: List[str] = []
        self.last_input = None
        self.yaml_file_name = "app.yml"
        self._execution_time_start = None

    def executing_first(self, lambda_func: Callable) -> "HexagonSpec":
        _log(self.executing_first, lambda_func=lambda_func)
        lambda_func(self)
        return self

    def given_a_cli_yaml(self, config: Union[str, Dict]) -> "HexagonSpec":
        _log(self.given_a_cli_yaml, config=config)
        if isinstance(config, str):
            self.yaml_file_name = config
        else:
            write_hexagon_config(self.test_dir, config)
        return self

    def run_hexagon(
        self,
        command: List[str] = None,
        os_env_vars: Optional[Dict[str, str]] = None,
        test_dir: Optional[str] = None,
    ) -> "HexagonSpec":
        print(f"\n\n[dim]RUNNING SPEC -> [/dim][b]{inspect.stack()[1][3]}[/b]")
        _log(
            self.run_hexagon,
            command=command,
            os_env_vars=os_env_vars,
            test_dir=test_dir,
        )
        __tracebackhide__ = True
        self._execution_time_start = time.time()
        if command:
            self.command = command
            self.test_dir, self.process = run_hexagon_e2e_test(
                self.__file,
                self.command,
                yaml_file_name=self.yaml_file_name,
                os_env_vars=os_env_vars,
                test_dir=test_dir or self.test_dir,
            )
        else:
            self.test_dir, self.process = run_hexagon_e2e_test(
                self.__file,
                yaml_file_name=self.yaml_file_name,
                os_env_vars=os_env_vars,
                test_dir=test_dir or self.test_dir,
            )
        return self

    def with_shared_behavior(self, func: Callable):
        _log(self.with_shared_behavior, func=func)
        __tracebackhide__ = True
        func(self)
        return self

    def then_output_should_be(
        self,
        expected_output: List[Expected_Process_Output],
        discard_until_first_match=False,
        ignore_blank_lines=True,
    ) -> "HexagonSpec":
        _log(
            self.then_output_should_be,
            expected_output=expected_output,
            discard_until_first_match=discard_until_first_match,
            ignore_blank_lines=ignore_blank_lines,
        )
        __tracebackhide__ = True
        self.lines_read = assert_process_output(
            self.process,
            expected_output,
            discard_until_first_match=discard_until_first_match,
            ignore_blank_lines=ignore_blank_lines,
            lines_read=self.lines_read,
        )
        return self

    def then_output_should_not_contain(
        self,
        output_to_match: List[Expected_Process_Output],
    ) -> "HexagonSpec":
        _log(self.then_output_should_not_contain, output_to_match=output_to_match)
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

    def arrow_down(self) -> "HexagonSpec":
        _log(self.arrow_down)
        __tracebackhide__ = True
        write_to_process(self.process, ARROW_DOWN_CHARACTER)
        return self

    def arrow_up(self) -> "HexagonSpec":
        _log(self.arrow_up)
        __tracebackhide__ = True
        write_to_process(self.process, ARROW_UP_CHARACTER)
        return self

    def enter(self) -> "HexagonSpec":
        _log(self.enter)
        __tracebackhide__ = True
        return self.write(LINE_FEED_CHARACTER)

    def space_bar(self) -> "HexagonSpec":
        _log(self.space_bar)
        __tracebackhide__ = True
        return self.write(SPACE_BAR_CHARACTER)

    def tab(self) -> "HexagonSpec":
        _log(self.tab)
        __tracebackhide__ = True
        return self.write(TAB_CHARACTER)

    def esc(self) -> "HexagonSpec":
        _log(self.esc)
        __tracebackhide__ = True
        return self.write(ESCAPE_CHARACTER)

    def carriage_return(self) -> "HexagonSpec":
        _log(self.carriage_return)
        __tracebackhide__ = True
        return self.write(CARRIAGE_RETURN_CHARACTER)

    def input(self, text: str) -> "HexagonSpec":
        _log(self.input, text=text)
        __tracebackhide__ = True
        self.last_input = text
        return self.write(f"{text}{LINE_FEED_CHARACTER}")

    def erase(self, val: Optional[Union[str, int]] = None) -> "HexagonSpec":
        _log(self.erase, val=val)
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

    def write(self, text: str) -> "HexagonSpec":
        __tracebackhide__ = True
        write_to_process(self.process, text)
        return self

    def exit(
        self, status: int = 0, timeout_in_seconds: int = 5, execution_time: int = None
    ) -> "HexagonSpec":
        _log(
            self.exit,
            status=status,
            timeout_in_seconds=timeout_in_seconds,
            execution_time=execution_time,
        )
        __tracebackhide__ = True
        assert_process_ended(
            self.process,
            exit_status=status,
            timeout_in_seconds=timeout_in_seconds,
            lines_read=self.lines_read,
        )
        if execution_time:
            assert_execution_time(
                time.time() - self._execution_time_start, execution_time
            )
        clean_hexagon_environment()
        return self

    def force_exit(self) -> "HexagonSpec":
        _log(self.force_exit)
        return self.write(CONTROL_C_CHARACTER)

    def wait(self, seconds: int) -> "HexagonSpec":
        _log(self.wait, seconds=seconds)
        time.sleep(seconds)
        return self

    @property
    def _and_(self) -> "HexagonSpec":
        return self


def as_a_user(test_file, test_dir=None) -> "HexagonSpec":
    return HexagonSpec(test_file, test_dir=test_dir)

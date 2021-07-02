from typing import List

from e2e.tests.utils.assertions import (
    Expected_Process_Output,
    assert_process_output,
    assert_process_ended,
)
from e2e.tests.utils.cli import ARROW_DOWN_CHARACTER
from e2e.tests.utils.run import run_hexagon_e2e_test, write_to_process


class HexagonSpec:
    def __init__(self, file) -> None:
        self.__file = file
        self.process = None
        self.command = None

    def run_hexagon(self, command=None):
        __tracebackhide__ = True
        if command:
            self.command = command
            self.process = run_hexagon_e2e_test(self.__file, self.command)
        else:
            self.process = run_hexagon_e2e_test(self.__file)
        return self

    def then_output_should_be(self, expected_output: List[Expected_Process_Output]):
        __tracebackhide__ = True
        assert_process_output(self.process, expected_output)
        return self

    def arrow_down(self):
        __tracebackhide__ = True
        write_to_process(self.process, ARROW_DOWN_CHARACTER)
        return self

    def enter(self):
        __tracebackhide__ = True
        write_to_process(self.process, "\n")
        return self

    def write(self, text: str):
        __tracebackhide__ = True
        write_to_process(self.process, text)
        return self

    def exit(self, status: int = 0):
        __tracebackhide__ = True
        assert_process_ended(self.process, status)


def as_a_user(test_file):
    return HexagonSpec(test_file)

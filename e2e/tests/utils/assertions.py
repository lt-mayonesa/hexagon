import collections
import subprocess
import os
from typing import Callable, List

last_output_file_path = os.path.realpath(os.path.join(
    __file__, os.path.pardir, os.path.pardir, os.path.pardir, 'last-output.txt'))


def _save_last_output(lines: List[str]):
    with open(last_output_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(lines))


def _save_last_output_and_raise(process: subprocess.Popen, lines_read: List[str], assertion_error: AssertionError):
    process.kill()
    lines: List[str] = [*lines_read, *process.stdout.readlines()]
    print('Last command output:')
    for line in lines:
        print(line.rstrip())
    _save_last_output(lines)
    raise assertion_error


Expected_Process_Output_Item = str or Callable[[str], bool]
Expected_Process_Output = Expected_Process_Output_Item or List[Expected_Process_Output_Item]


def _assert_process_output_line(
    process: subprocess.Popen,
    line: str,
    expected: Expected_Process_Output,
    lines_read: List[str],
    to_discard_count: int
):
    def assert_line(expected: Expected_Process_Output_Item):
        if isinstance(expected, str):
            assert expected.rstrip() in line.rstrip()
        if isinstance(expected, collections.Callable):
            assert expected(line)
    try:
        if isinstance(expected, list):
            for assertion in expected:
                assert_line(assertion)
        else:
            assert_line(expected)
    except AssertionError as assertion_error:
        # Check if the command failed and show the failure message
        if process.returncode and process.returncode > 0:
            raise Exception('\n'.join(process.stderr.readlines()))
        else:
            if to_discard_count > 0:
                return False
            _save_last_output_and_raise(process, lines_read, assertion_error)

    return True


def assert_process_output(
    process: subprocess.Popen,
    expected_output: List[Expected_Process_Output],
    discard_until_initial=False
):
    """
    Assert the output of a CLI process

    Params:
        * `process`: The process, usualy instantiaded using `e2e.test.utils.run.run_hexagon_e2e_test`
        * `expected_output`: Expected lines to be compared with the actual output lines. Possible types:
            - String to be searched in the output line
            - Predicate that receives the line
            - List of strings and/or predicates
        * `discard_until_initial`: Discard lines until the first expected line is found.
            There will be as many attempts to find the first match as expected lines passed

    Expecting more lines than those present in the output will cause a deadlock
    """
    line_index = 0
    lines_read = []
    to_discard_count = len(expected_output) if discard_until_initial else 0
    # Read from stdout until assertion fails or all expected lines are read
    # Attempting to read more lines than available will result in a deadlock, we should put a short timeout here.
    # Test-level tiemouts will either be too short or too long because a test can have many output assertions
    while line_index < len(expected_output):
        line: str = process.stdout.readline()
        lines_read.append(line)

        expected = expected_output[line_index]

        if not _assert_process_output_line(
            process,
            line,
            expected,
            lines_read,
            to_discard_count
        ):
            to_discard_count -= 1

        line_index += 1

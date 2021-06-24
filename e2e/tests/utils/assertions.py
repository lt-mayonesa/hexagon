import subprocess
import os
from functools import partial
from typing import List

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


def assert_process_output(process: subprocess.Popen, expected_output: List[str], discard_until_initial=False):
    line_index = 0
    lines_read = []
    to_discard_count = len(expected_output) if discard_until_initial else 0
    # Read from stdout until assertion fails or all expected lines are read
    # Attempting to read more lines than available will result in a deadlock, we should put a short timeout here.
    # Test-level tiemouts will either be too short or too long because a test can have many output assertions
    while line_index < len(expected_output):
        line: str = process.stdout.readline()
        lines_read.append(line)

        try:
            assert expected_output[line_index].rstrip() in line.rstrip()
        except AssertionError as assertion_error:
            if to_discard_count > 0:
                to_discard_count -= 1
                continue
            handle_assertion_error = partial(_save_last_output_and_raise, process, lines_read, assertion_error)
            # Check if the command failed and show the failure message
            if not line:
                err_lines = process.stderr.readlines()
                if len(err_lines) > 0:
                    raise Exception('\n'.join(err_lines))
                else:
                    handle_assertion_error()
            else:
                handle_assertion_error()

        line_index += 1

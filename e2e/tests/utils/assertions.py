import subprocess
import os
import signal
import re
from typing import Callable, List

last_output_file_path = os.path.realpath(
    os.path.join(
        __file__, os.path.pardir, os.path.pardir, os.path.pardir, "last-output.txt"
    )
)


def _save_last_output(lines: List[str]):
    with open(last_output_file_path, "w", encoding="utf-8") as file:
        file.write("".join(lines))


def _save_last_output_and_raise(
    process: subprocess.Popen, lines_read: List[str], error: Exception, timeouted=False
):
    __tracebackhide__ = True
    process.kill()
    lines: List[str] = [*lines_read]
    if not timeouted:
        for line in process.stdout.readlines():
            lines.append(line)
    print("command output:")
    for line in lines:
        print(line.rstrip())

    print(process.stderr.read())

    _save_last_output(lines)
    raise error


def _check_process_return_code(process: subprocess.Popen, exit_status: int = 0):
    __tracebackhide__ = True
    if process.returncode and process.returncode > exit_status:
        raise Exception("\n".join(process.stderr.readlines()))
    elif process.returncode:
        assert process.returncode == exit_status


Expected_Process_Output_Item = str or Callable[[str], bool]
Expected_Process_Output = (
    Expected_Process_Output_Item or List[Expected_Process_Output_Item]
)


ansi_escape_regex = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def ansi_escape(text: str):
    return ansi_escape_regex.sub("", text)


def single_assert_line(line: str, expected: Expected_Process_Output_Item):
    __tracebackhide__ = True
    if isinstance(expected, str):
        try:
            assert expected.rstrip() in line.rstrip()
        except AssertionError:
            raise Exception(
                "\n".join(
                    [
                        "Failed to match hexagon output:"
                        f"\nExpected: \033[92m{ansi_escape(expected.rstrip())}",
                        f"Got: \033[93m{ansi_escape(line.rstrip())}",
                    ]
                )
            ) from None

    if isinstance(expected, Callable):
        assert expected(line)


def _assert_process_output_line(
    process: subprocess.Popen,
    line: str,
    expected: Expected_Process_Output,
    lines_read: List[str],
    discard_until_initial: bool,
):
    __tracebackhide__ = True
    try:
        if isinstance(expected, list):
            for assertion in expected:
                single_assert_line(line, assertion)
        else:
            single_assert_line(line, expected)
    except Exception as error:
        _check_process_return_code(process)

        if discard_until_initial:
            return False

        _save_last_output_and_raise(process, lines_read, error)

    return True


MAX_ATTEMPTS = 50


def assert_process_output(
    process: subprocess.Popen,
    expected_output: List[Expected_Process_Output],
    discard_until_initial=False,
):
    """
    Assert the output of a CLI process

    Possible types for expected_output:
        - String to be searched in the output line
        - Predicate that receives the line
        - List of strings and/or predicates

    :param process: The process, usualy instantiaded using `e2e.test.utils.run.run_hexagon_e2e_test`
    :param expected_output: Expected lines to be compared with the actual output lines.
    :param discard_until_initial: Discard lines until the first expected line is found
    :return:
    """
    __tracebackhide__ = True
    line_index = 0
    lines_read = []
    attempts = 0
    # Read from stdout until assertion fails or all expected lines are reads
    while line_index < len(expected_output):

        def timeout_handler(signum, frame):
            _save_last_output_and_raise(
                process,
                lines_read,
                Exception("Timeout reading from process"),
                timeouted=True,
            )

        signal.signal(signal.SIGALRM, timeout_handler)

        signal.alarm(3)
        line: str = process.stdout.readline()
        signal.alarm(0)

        lines_read.append(line)

        expected = expected_output[line_index]

        if _assert_process_output_line(
            process, line, expected, lines_read, discard_until_initial
        ):
            line_index += 1
        else:
            if attempts >= MAX_ATTEMPTS:
                _save_last_output_and_raise(
                    process,
                    lines_read,
                    Exception(f"Couldnt match output after {MAX_ATTEMPTS} attempts"),
                )
            attempts += 1


def assert_process_ended(process: subprocess.Popen, exit_status: int = 0):
    __tracebackhide__ = True
    try:
        process.wait(5)
    except Exception as error:
        _save_last_output_and_raise(process, [], error)

    _check_process_return_code(process, exit_status)

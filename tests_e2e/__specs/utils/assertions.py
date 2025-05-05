import os
import re
import signal
import subprocess
import sys
from typing import Any, Callable, Dict, List

from tests_e2e.__specs.utils.console import print
from tests_e2e.__specs.utils.path import e2e_test_folder_path

last_output_file_path = os.path.realpath(
    os.path.join(
        __file__, os.path.pardir, os.path.pardir, os.path.pardir, "last-output.txt"
    )
)


def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    # Check for standard trace function
    gettrace = hasattr(sys, "gettrace") and sys.gettrace() is not None

    # Check for PyCharm debugger
    pydev_debugger = "pydevd" in sys.modules

    # Check for VSCode debugger
    vscode_debugger = any(mod.startswith("debugpy") for mod in sys.modules)

    # Check for environment variable some debuggers might set
    env_debugger = os.environ.get("PYTHONBREAKPOINT") is not None

    return gettrace or pydev_debugger or vscode_debugger or env_debugger


def _save_last_output(lines: List[str]):
    with open(last_output_file_path, "w", encoding="utf-8") as file:
        file.write("".join(lines))


def _save_last_output_and_raise(
    process: subprocess.Popen,
    lines_read: List[str],
    error: Exception = None,
    timeout_reached=False,
):
    __tracebackhide__ = True
    process.kill()
    lines: List[str] = [*lines_read]
    if not timeout_reached:
        for line in process.stdout.readlines():
            lines.append(line)
    print("\n[u]command stdout:\n")
    for line in lines:
        print(line.rstrip())

    print("\n[u]command stderr:\n")
    for line in process.stderr.readlines():
        print(line.rstrip())

    _save_last_output(lines)
    if error:
        raise error


def _check_process_return_code(process: subprocess.Popen, exit_status: int = 0):
    __tracebackhide__ = True
    return_code = process.returncode
    if type(return_code) is int:
        error = "\n".join(process.stderr.readlines())
        assert return_code == exit_status, (
            f"Got return_code {return_code}, but {exit_status} was expected\n"
            f"Terminal error:\n" + error
        )


Expected_Process_Output_Item = str or Callable[[str], bool] or Dict[str, Any]
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


def _read_next_line(process: subprocess.Popen, lines_read: List[str]):
    def timeout_handler(signum, frame):
        _save_last_output_and_raise(
            process,
            lines_read,
            Exception("Timeout reading from process"),
            timeout_reached=True,
        )

    signal.signal(signal.SIGALRM, timeout_handler)

    if not debugger_is_active():
        signal.alarm(10)
    line: str = process.stdout.readline()
    signal.alarm(0)

    lines_read.append(line)

    return line


def _assert_expected_text(line: str, expected: str or List[str]):
    if isinstance(expected, list):
        for assertion in expected:
            single_assert_line(line, assertion)
    else:
        single_assert_line(line, expected)


def _assert_dynamic_line_width(
    process: subprocess.Popen,
    line: str,
    error: Exception,
    expected: Expected_Process_Output,
    lines_read: List[str],
    text: str,
):
    if "max_lines" in expected and isinstance(expected["max_lines"], int):
        line_delimiter = "\n"
        if "line_delimiter" in expected and isinstance(expected["line_delimiter"], str):
            line_delimiter = expected["line_delimiter"]
        max_lines = expected["max_lines"]
        accumulated_line = line
        number_of_lines_read = 1
        last_error = error
        while number_of_lines_read < max_lines:
            accumulated_line += _read_next_line(process, lines_read)
            accumulated_line = accumulated_line.replace(line_delimiter, "")
            try:
                _assert_expected_text(accumulated_line, text)
                return True
            except Exception as last:
                number_of_lines_read += 1
                last_error = last
        raise last_error
    else:
        raise error


def _assert_process_output_line(
    process: subprocess.Popen,
    line: str,
    expected: Expected_Process_Output,
    lines_read: List[str],
    discard_until_initial: bool,
):
    __tracebackhide__ = True
    try:
        if isinstance(expected, dict):
            text = expected["expected"]
            if not text:
                raise Exception(
                    "Expected config object must contain the expected text in the expected property"
                )
            try:
                _assert_expected_text(line, text)
            except Exception as error:
                _assert_dynamic_line_width(
                    process, line, error, expected, lines_read, text
                )
        _assert_expected_text(line, expected)
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
    discard_until_first_match=False,
    ignore_blank_lines=True,
    lines_read: List[str] = None,
):
    """
    Assert the output of a CLI process

    Possible types for expected_output:
        - String to be searched in the output line
        - Predicate that receives the line
        - List of strings and/or predicates

    :param process: The process, usually instantiated using `tests_e2e.test.utils.run.run_hexagon_e2e_test`
    :param expected_output: Expected lines to be compared with the actual output lines.
    :param discard_until_first_match: Discard lines until the first expected line is found
    :param ignore_blank_lines: If line is blank ("\n"), ignore it
    :param lines_read: List to accumulate the lines read from the process
    :return:
    """
    __tracebackhide__ = True
    line_index = 0
    lines_read = lines_read or []
    attempts = 0
    # Read from stdout until assertion fails or all expected lines are reads
    while line_index < (
        1 if isinstance(expected_output, str) else len(expected_output)
    ):
        line: str = _read_next_line(process, lines_read)
        expected = expected_output[line_index]

        if ignore_blank_lines and _is_linebreak(line):
            continue

        if _assert_process_output_line(
            process, line, expected, lines_read, discard_until_first_match
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

    return lines_read


def assert_process_ended(
    process: subprocess.Popen,
    exit_status: int = 0,
    timeout_in_seconds: int = 5,
    lines_read: List[str] = None,
):
    __tracebackhide__ = True

    if debugger_is_active():
        timeout_in_seconds = 60 * 5  # 5 minutes

    err = None
    try:
        process.wait(timeout_in_seconds)
    except Exception as error:
        err = error

    _save_last_output_and_raise(process, lines_read or [], err)
    _check_process_return_code(process, exit_status)


def assert_execution_time(elapsed: int, expected: int):
    __tracebackhide__ = True
    assert (
        elapsed <= expected
    ), f"Execution time {elapsed}ms is greater than expected {expected}ms"


def assert_file_has_contents(test_file: str, file: str, contents: str):
    test_dir = e2e_test_folder_path(test_file)

    with open(os.path.join(test_dir, file), "r") as f:
        assert f.read() == contents


def assert_file_does_not_exist(test_file: str, file: str):
    test_dir = e2e_test_folder_path(test_file)
    assert os.path.isfile(os.path.join(test_dir, file)) is False


def _is_linebreak(line):
    """
    Check if line is a linebreak.
    A linebreak is a string containing a trailing linebreak character ("\n"),
    and 0 or any number of leading whitespace characters
    :param line:
    :return:
    """
    return re.match(r"^\s*\n$", line)

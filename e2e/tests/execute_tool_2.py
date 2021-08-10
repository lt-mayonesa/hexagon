from e2e.tests.utils.assertions import (
    assert_file_has_contents,
)
from e2e.tests.utils.hexagon_spec import as_a_user

shared_prompt_output = [
    "Hi, which tool would you like to use today?",
    "┌──────────────────────────────────────────────────────────────────────────────",
    "",
    "",
    "",
    "ƒ A generic command",
    "",
    "ƒ A complex command",
    "",
    "ƒ A generic multinline command",
    "",
    "ƒ A failing command",
    "",
    "ƒ Python Module File Test",
    "",
    "ƒ Python Module Import Error Test",
    "",
    "ƒ Python Module Script Error Test",
    "",
    "└──────────────────────────────────────────────────────────────────────────────",
    "",
]


def test_show_correct_error_when_execute_python_module_with_import_error():
    (
        as_a_user(__file__)
        .run_hexagon(["p-m-import-error"])
        .then_output_should_be(
            [
                "╭───────────────────── Traceback (most recent call last) ──────────────────────╮",
                "p-m-import-error.py:4",
                "",
                "",
                "1",
                "2",
                "3",
                "4 from hexagon.cli.env import Env",
                "5",
                "6",
            ]
        )
        .exit(status=1)
    )


def test_show_correct_error_when_execute_python_module_with_script_error():
    (
        as_a_user(__file__)
        .run_hexagon(["p-m-script-error"])
        .then_output_should_be(
            [
                "executed p-m-script-error",
                "╭───────────────────── Traceback (most recent call last) ──────────────────────╮",
                "p-m-script-error.py:15",
                "",
                "",
                "12",
                "13",
                "14",
                "15 │   err = [][3]",
                "16",
                "17",
                "18",
                "─────────────────────────────────────────────────────────────────────",
                "IndexError: list index out of range",
                "Execution of tool p-m-script-error failed",
            ]
        )
        .exit(status=1)
    )


def test_execute_command():
    (
        as_a_user(__file__)
        .run_hexagon(["generic-command"])
        .then_output_should_be(["executed generic-command"])
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test generic-command"
    )


def test_execute_complex_command():
    (
        as_a_user(__file__)
        .run_hexagon(["complex-command"])
        .then_output_should_be(["nested 1"])
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test complex-command"
    )


def test_execute_multiline_command():
    (
        as_a_user(__file__)
        .run_hexagon(["generic-multiline-command"])
        .then_output_should_be(
            [
                "executed generic-multiline-command #1",
                "executed generic-multiline-command #2",
                "executed generic-multiline-command #3",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test generic-multiline-command",
    )


def test_execute_failing_command():
    (
        as_a_user(__file__)
        .run_hexagon(["failing-command"], {"HEXAGON_THEME": "default"})
        .then_output_should_be(
            [
                "i-dont-exist returned code: 127",
                "Hexagon couldn't execute the action: i-dont-exist",
                "We tried:",
            ],
            True,
        )
        .exit(1)
    )

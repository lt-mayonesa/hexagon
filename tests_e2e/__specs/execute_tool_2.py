import os

from tests_e2e.__specs.utils.assertions import assert_file_has_contents
from tests_e2e.__specs.utils.hexagon_spec import as_a_user

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
                "╭─────────────────────────────── Traceback (most recent call last) ────────────────────────────────╮",
                {
                    "expected": "p_m_import_error.py",
                    "max_lines": 2,
                    "line_delimiter": " │\n│ ",
                },
            ]
        )
        .then_output_should_be(
            [
                "from hexagon.cli.env import Env",
            ],
            discard_until_first_match=True,
        )
        .then_output_should_be(
            [
                "ModuleNotFoundError: No module named 'hexagon.cli'",
                "Your custom action seems to have a module dependency error",
            ],
            discard_until_first_match=True,
        )
        .exit(status=1)
    )


def test_show_correct_error_when_execute_python_module_with_script_error():
    (
        as_a_user(__file__)
        .run_hexagon(["p-m-script-error"])
        .then_output_should_be(
            [
                "executed p_m_script_error",
                "╭─────────────────────────────── Traceback (most recent call last) ────────────────────────────────╮",
                {
                    "expected": ["p_m_script_error.py:15"],
                    "max_lines": 2,
                    "line_delimiter": " │\n│ ",
                },
            ]
        )
        .then_output_should_be(
            [
                "12",
                "13",
                "14",
                "15 │   err = [][3]",
                "16",
                "17",
                "18",
                "─────────────────────────────────────────────────────────────────────",
                "IndexError: list index out of range",
                "Execution of tool p_m_script_error failed",
            ],
            discard_until_first_match=True,
        )
        .exit(status=1)
    )


def test_show_correct_error_when_execute_python_module_with_script_error_and_no_custom_tools_dir():
    (
        as_a_user(__file__)
        .given_a_cli_yaml("app_no_custom_tools_dir.yml")
        .run_hexagon(["p-m-script-error"])
        .then_output_should_be(
            [
                "executed p_m_script_error",
                "╭─────────────────────────────── Traceback (most recent call last) ────────────────────────────────╮",
                {
                    "expected": ["action.py"],
                    "max_lines": 2,
                    "line_delimiter": " │\n│ ",
                },
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


def test_execute_complex_command_with_dots():
    (
        as_a_user(__file__)
        .run_hexagon(["complex-command-with-dots"])
        .then_output_should_be(["with . dots hexagon"])
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test complex-command-with-dots",
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


def test_execute_multiline_command_with_input_as_list():
    (
        as_a_user(__file__)
        .run_hexagon(["multiline-command-as-list"])
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
        "hexagon-test multiline-command-as-list",
    )


def test_execute_a_formatted_command_with_env_args():
    (
        as_a_user(__file__)
        .run_hexagon(["a-simple-formatted-command", "dev"])
        .then_output_should_be(["environment: development, tool: A formatted command"])
        .exit()
    )
    (
        as_a_user(__file__)
        .run_hexagon(["a-simple-formatted-command", "qa"])
        .then_output_should_be(
            ["environment: quality assurance, tool: A formatted command"]
        )
        .exit()
    )


def test_execute_a_formatted_command_with_object_env_args():
    (
        as_a_user(__file__)
        .run_hexagon(["a-complex-formatted-command", "dev"])
        .then_output_should_be(["Hello John, you are 30 years old"])
        .exit()
    )
    (
        as_a_user(__file__)
        .run_hexagon(["a-complex-formatted-command", "qa"])
        .then_output_should_be(["Hello Jane, you are 40 years old"])
        .exit()
    )


def test_execute_a_formatted_command_with_all_action_args():
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "all-tool-args-are-replaced",
                "dev",
                "cli_positional_value",
                "--cli_optional='value'",
            ]
        )
        .then_output_should_be(
            [
                "tool alias is ataar, selected env is dev",
                "env_args is 32, cli_args are cli_positional_value and 'value'",
            ]
        )
        .exit()
    )


def test_execute_inline_command_with_path():
    path = os.environ["PATH"]
    (
        as_a_user(__file__)
        .run_hexagon(["inline-command-with-PATH"])
        .then_output_should_be([path])
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test inline-command-with-PATH",
    )


def test_execute_failing_command():
    (
        as_a_user(__file__)
        .run_hexagon(["failing-command"], {"HEXAGON_THEME": "no_border"})
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

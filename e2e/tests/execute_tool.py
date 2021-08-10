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
    "⦾ Google",
    "",
    "ƒ Python Module Test",
    "",
    "ƒ Python Module Env Test",
    "",
    "ƒ Python Module Asterisk Env Test",
    "",
    "ƒ Node Module Test",
    "",
    "ƒ Node Module Env Test",
    "",
    "",
    "",
    "",
    "",
    "└──────────────────────────────────────────────────────────────────────────────",
    "",
]


def test_execute_python_module_by_gui():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(shared_prompt_output)
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "ƒ Python Module Test"],
                "executed python-module",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test python-module"
    )


def test_execute_python_module_with_env_by_gui():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(shared_prompt_output)
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                [
                    "Hi, which tool would you like to use today?",
                    "ƒ Python Module Env Test",
                ],
            ]
        )
        .then_output_should_be(
            ["On which environment?", "", "", "", "", "dev", "", "qa", "", "", ""]
        )
        .enter()
        .then_output_should_be(
            [
                ["On which environment?", "dev"],
                "executed python-module",
                "Env:",
                "alias='d' long_name='dev' description=None",
                "Env args:",
                "[789, 'ghi']",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test python-module-env dev"
    )


def test_execute_python_module_with_env_asterisk_by_gui():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(shared_prompt_output)
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                [
                    "Hi, which tool would you like to use today?",
                    "ƒ Python Module Asterisk Env Test",
                ],
                "",
                "executed python-module",
                "Env args:",
                "all_envs",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test python-module-env-all"
    )


def test_execute_python_module_by_argument():
    (
        as_a_user(__file__)
        .run_hexagon(["python-module"])
        .then_output_should_be(
            [
                "executed python-module",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test python-module"
    )


def test_execute_python_module_by_alias():
    (
        as_a_user(__file__)
        .run_hexagon(["pm"])
        .then_output_should_be(
            [
                "executed python-module",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test python-module"
    )


def test_execute_python_module_with_env_and_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(["python-module-env", "dev", "123", "abc"])
        .then_output_should_be(
            [
                "executed python-module",
                "Env:",
                "alias='d' long_name='dev' description=None",
                "Env args:",
                "[789, 'ghi']",
                "Cli args:",
                "123",
                "abc",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test python-module-env dev"
    )


def test_execute_python_module_with_other_env():
    (
        as_a_user(__file__)
        .run_hexagon(["python-module-env", "qa"])
        .then_output_should_be(
            [
                "executed python-module",
                "Env:",
                "alias='q' long_name='qa' description=None",
                "Env args:",
                "ordereddict([('foo', 'foo'), ('bar', 'bar')])",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test python-module-env qa"
    )


def test_execute_script_module_by_gui():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(shared_prompt_output)
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "ƒ Node Module Test"],
                "executed node module",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test node-module"
    )


def test_execute_script_module_by_argument():
    (
        as_a_user(__file__)
        .run_hexagon(["node-module"])
        .then_output_should_be(
            [
                "executed node module",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test node-module"
    )


def test_execute_script_module_with_env_and_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(["node-module-env", "dev", "arg1", "arg2"])
        .then_output_should_be(
            [
                "executed node module",
                "CLI arguments:",
                "789",
                "ghi",
                "long_name='dev' description=None",
                "arg1",
                "arg2",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test node-module-env dev"
    )


def test_execute_script_module_with_other_env():
    (
        as_a_user(__file__)
        .run_hexagon(["node-module-env", "qa"])
        .then_output_should_be(
            [
                "executed node module",
                "CLI arguments:",
                "foo=foo",
                "bar=bar",
                "long_name='qa' description=None",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test node-module-env qa"
    )

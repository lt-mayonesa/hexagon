from tests_e2e.__specs.utils.assertions import assert_file_has_contents
from tests_e2e.__specs.utils.hexagon_spec import HexagonSpec, as_a_user


def _shared_assertions(spec: HexagonSpec):
    (
        spec.then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "9/9",
                "⦾ Google",
                "ƒ Python Module Test",
                "ƒ Python Module Env Test",
                "ƒ Python Module Asterisk Env Test",
                "ƒ Node Module Test",
                "ƒ Node Module Env Test",
                "ƒ Python Module Single File Test",
                "⬡ Save Last Command as Shell Alias",
            ]
        )
    )


def test_execute_python_module_by_gui():
    (
        as_a_user(__file__)
        .run_hexagon()
        .with_shared_behavior(_shared_assertions)
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "ƒ Python Module Test"],
                "executed python_module",
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
        .with_shared_behavior(_shared_assertions)
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
            [
                "On which environment?",
                "2/2",
                "dev",
                "qa",
            ]
        )
        .enter()
        .then_output_should_be(
            [
                ["On which environment?", "dev"],
                "executed python_module",
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
        .with_shared_behavior(_shared_assertions)
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
                "executed python_module",
                "Env args:",
                "all_envs",
            ],
            ignore_blank_lines=False,
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
        .then_output_should_be(["executed python_module"])
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test python-module"
    )


def test_execute_python_module_by_alias():
    (
        as_a_user(__file__)
        .run_hexagon(["pm"])
        .then_output_should_be(["executed python_module"])
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
                "executed python_module",
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
                "executed python_module",
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
        .with_shared_behavior(_shared_assertions)
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
        .then_output_should_be(["executed node module"])
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
                "arg1",
                "arg2",
                "envvars:",
                'HEXAGON_EXECUTION_TOOL = {"name": "node-module-env", "type": "shell", "icon": null, "alias": "nme", "long_name": "Node Module Env Test", "description": null, "envs": {"dev": [789, "ghi"], "qa": {"foo": "foo", "--bar": "bar"}}, "traced": true, "action": "node-module.js"}',  # noqa: E501
                'HEXAGON_EXECUTION_ENV = {"name": "dev", "alias": "d", "long_name": "dev", "description": null}',
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
                "--bar=bar",
                "envvars:",
                'HEXAGON_EXECUTION_TOOL = {"name": "node-module-env", "type": "shell", "icon": null, "alias": "nme", "long_name": "Node Module Env Test", "description": null, "envs": {"dev": [789, "ghi"], "qa": {"foo": "foo", "--bar": "bar"}}, "traced": true, "action": "node-module.js"}',  # noqa: E501
                'HEXAGON_EXECUTION_ENV = {"name": "qa", "alias": "q", "long_name": "qa", "description": null}',
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__, ".config/test/last-command.txt", "hexagon-test node-module-env qa"
    )


def test_execute_single_file_python_module_by_gui():
    (
        as_a_user(__file__)
        .run_hexagon()
        .with_shared_behavior(_shared_assertions)
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                [
                    "Hi, which tool would you like to use today?",
                    "ƒ Python Module Single File Test",
                ],
                "executed single_file_module",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test single-file-python-module",
    )

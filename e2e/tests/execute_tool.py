from e2e.tests.utils.hexagon_spec import as_a_user

shared_prompt_output = [
    "╭╼ Test",
    "│",
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
    "⬡ Save Last Command",
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
                "│",
                "╰╼",
                "Para repetir este comando:",
                "    hexagon-test python-module",
            ]
        )
        .exit()
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
                "Env args:",
                "[789, 'ghi']",
                "│",
                "╰╼",
                "Para repetir este comando:",
                "    hexagon-test python-module",
            ]
        )
        .exit()
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
                "│",
                "╰╼",
                "Para repetir este comando:",
                "    hexagon-test python-module",
            ]
        )
        .exit()
    )


def test_execute_python_module_by_argument():
    (
        as_a_user(__file__)
        .run_hexagon(["python-module"])
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "executed python-module",
                "│",
                "╰╼",
            ]
        )
        .exit()
    )


def test_execute_python_module_by_alias():
    (
        as_a_user(__file__)
        .run_hexagon(["pm"])
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "executed python-module",
                "│",
                "╰╼",
            ]
        )
        .exit()
    )


def test_execute_python_module_with_env_and_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(["python-module-env", "dev", "123", "abc"])
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "executed python-module",
                "Env:",
                "ordereddict([('alias', 'd'), ('name', 'dev')])",
                "Env args:",
                "[789, 'ghi']",
                "Cli args:",
                "123",
                "abc",
                "│",
                "╰╼",
            ]
        )
        .exit()
    )


def test_execute_python_module_with_other_env():
    (
        as_a_user(__file__)
        .run_hexagon(["python-module-env", "qa"])
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "executed python-module",
                "Env:",
                "ordereddict([('alias', 'q'), ('name', 'qa')])",
                "Env args:",
                "ordereddict([('foo', 'foo'), ('bar', 'bar')])",
                "│",
                "╰╼",
            ]
        )
        .exit()
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
                "│",
                "╰╼",
                "Para repetir este comando:",
                "    hexagon-test node-module",
            ]
        )
        .exit()
    )


def test_execute_script_module_by_argument():
    (
        as_a_user(__file__)
        .run_hexagon(["node-module"])
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "executed node module",
                "│",
                "╰╼",
            ]
        )
        .exit()
    )


def test_execute_script_module_with_env_and_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(["node-module-env", "dev", "arg1", "arg2"])
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "executed node module",
                "CLI arguments:",
                "name=dev",
                "789",
                "ghi",
                "arg1",
                "arg2",
                "│",
                "╰╼",
            ]
        )
        .exit()
    )


def test_execute_script_module_with_other_env():
    (
        as_a_user(__file__)
        .run_hexagon(["node-module-env", "qa"])
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "executed node module",
                "CLI arguments:",
                "foo=foo",
                "bar=bar",
                "name=qa",
                "│",
                "╰╼",
            ]
        )
        .exit()
    )

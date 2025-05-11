from tests_e2e.__specs.utils.hexagon_spec import as_a_user


def test_execute_tool_group_from_gui():
    (
        as_a_user(__file__)
        .run_hexagon()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [["Hi, which tool would you like to use today?", "A group of tools"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["executed python_module"], True)
        .exit()
    )


def test_execute_tool_group_with_no_alias_from_gui():
    (
        as_a_user(__file__)
        .run_hexagon()
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                [
                    "Hi, which tool would you like to use today?",
                    "A group of tools with a custom",
                ]
            ],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(
            ["custom tools directory action"], discard_until_first_match=True
        )
        .exit()
    )


def test_execute_tool_from_ui_after_leaving_tool_group():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        # Select the first group
        .arrow_down()
        .enter()
        .then_output_should_be(
            [["Hi, which tool would you like to use today?", "A group of tools"]],
            discard_until_first_match=True,
        )
        # Go back to previous (root) menu
        .arrow_down(times=2)
        .enter()
        .then_output_should_be(["Go back"], discard_until_first_match=True)
        # Run an echo tool in the main app.yml file
        .arrow_down(times=4)
        .then_output_should_be(
            ["Hi, which tool would you like to use today?"],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["top level echo"], discard_until_first_match=True)
        .then_output_should_be(
            ["hexagon-test top-level-echo"], discard_until_first_match=True
        )
        .exit()
    )


def test_execute_tool_group_by_argument():
    (
        as_a_user(__file__)
        .run_hexagon(["group", "python-module"])
        .then_output_should_be(["executed python_module"])
        .exit()
    )


def test_execute_tool_group_by_argument_with_inherited_env_and_cli_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(["group", "python-module-env", "dev", "123", "abc"])
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


def test_execute_tool_group_by_argument_with_custom_tools_dir():
    (
        as_a_user(__file__)
        .run_hexagon(["custom-tools-dir-group", "echo"])
        .then_output_should_be(["custom tools directory action"])
        .exit()
    )


def test_execute_tool_group_in_different_directory_with_default_custom_tools_dir():
    (
        as_a_user(__file__)
        .run_hexagon(["group-in-dir", "echo"])
        .then_output_should_be(["group tools in dir"])
        .exit()
    )


def test_execute_tool_group_has_correct_trace():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        .arrow_down()
        .enter()
        .then_output_should_be(
            [["Hi, which tool would you like to use today?", "A group of tools"]],
            discard_until_first_match=True,
        )
        .arrow_down()
        .enter()
        .then_output_should_be(
            [["Hi, which tool would you like to use today?", "Python Module Env Test"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(
            ["hexagon-test group python-module-env dev"], discard_until_first_match=True
        )
        .exit()
    )


def test_execute_tool_inside_inline_group():
    (
        as_a_user(__file__)
        .run_hexagon(["inline-group", "echo-2"])
        .then_output_should_be(["inline tool 2"])
        .exit()
    )

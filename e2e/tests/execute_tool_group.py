from e2e.tests.utils.hexagon_spec import as_a_user


def test_execute_tool_group_from_ui():
    (
        as_a_user(__file__)
        .run_hexagon()
        .arrow_down()
        .enter()
        .enter()
        .then_output_should_be(["executed python-module"], True)
        .exit()
    )


def test_execute_tool_from_ui_after_leaving_tool_group():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "default"})
        # Select the first group
        .arrow_down()
        .enter()
        # Go back to previous (root) menu
        .arrow_down()
        .arrow_down()
        .enter()
        # Run an echo tool in the main app.yml file
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(["top level echo"], True)
        .then_output_should_be(["hexagon-test top-level-echo"], True)
        .exit()
    )


def test_execute_tool_group_by_argument():
    (
        as_a_user(__file__)
        .run_hexagon(["group", "python-module"])
        .then_output_should_be(["executed python-module"])
        .exit()
    )


def test_execute_tool_group_by_argument_with_inherited_env_and_cli_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(["group", "python-module-env", "dev", "123", "abc"])
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
    )


def test_execute_tool_group_has_correct_trace():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "default"})
        .arrow_down()
        .enter()
        .arrow_down()
        .enter()
        .enter()
        .then_output_should_be(["hexagon-test group python-module-env dev"], True)
        .exit()
    )

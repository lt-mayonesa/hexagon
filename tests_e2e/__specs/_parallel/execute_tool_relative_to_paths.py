from tests_e2e.framework.hexagon_spec import as_a_user


def test_execute_script_in_same_dir():
    (
        as_a_user(__file__)
        .given_a_cli_yaml("nested_cli/app.yml")
        .run_hexagon(["bash-script", "arg1", "arg2"])
        .then_output_should_be(
            [
                "bash_module from tests_e2e/execute_tool_relative_to_paths/nested_cli",
                "arguments:",
                "arg1",
                "arg2",
            ]
        )
        .exit()
    )


def test_execute_script_in_nested_to_parent_as_command():
    (
        as_a_user(__file__)
        .given_a_cli_yaml("nested_cli/app.yml")
        .run_hexagon(["bash-script-nested-as-command", "arg1", "arg2"])
        .then_output_should_be(
            [
                "bash_module from tests_e2e/execute_tool_relative_to_paths/nested_dir/level_1",
                "arguments:",
                "arg1",
                "arg2",
            ]
        )
        .exit()
    )


def test_execute_script_in_nested_to_parent_as_script():
    (
        as_a_user(__file__)
        .given_a_cli_yaml("nested_cli/app.yml")
        .run_hexagon(["bash-script-nested-as-script", "arg1", "arg2"])
        .then_output_should_be(
            [
                "bash_module from tests_e2e/execute_tool_relative_to_paths/nested_dir/level_1",
                "arguments:",
                "arg1",
                "arg2",
            ]
        )
        .exit()
    )


def test_execute_script_in_nested_dotted_parent():
    (
        as_a_user(__file__)
        .given_a_cli_yaml("nested_cli/app.yml")
        .run_hexagon(["bash-script-dotted", "arg1", "arg2"])
        .then_output_should_be(
            [
                "bash_module from tests_e2e/execute_tool_relative_to_paths/.dotted_dir/level_1",
                "arguments:",
                "arg1",
                "arg2",
            ]
        )
        .exit()
    )


def test_execute_script_access_with_weird_pathing():
    (
        as_a_user(__file__)
        .given_a_cli_yaml("nested_cli/app.yml")
        .run_hexagon(["bash-script-weird-path", "arg1", "arg2"])
        .then_output_should_be(
            [
                "bash_module from tests_e2e/execute_tool_relative_to_paths/.dotted_dir/level_2",
                "arguments:",
                "arg1",
                "arg2",
            ]
        )
        .exit()
    )


def test_execute_script_in_parent():
    (
        as_a_user(__file__)
        .given_a_cli_yaml("nested_cli/app.yml")
        .run_hexagon(["bash-script-parent", "arg1", "arg2"])
        .then_output_should_be(
            [
                "bash_module from tests_e2e/execute_tool_relative_to_paths",
                "arguments:",
                "arg1",
                "arg2",
            ]
        )
        .exit()
    )

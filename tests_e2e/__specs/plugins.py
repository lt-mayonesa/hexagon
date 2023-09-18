import os

from tests_e2e.__specs.utils.hexagon_spec import as_a_user
from tests_e2e.__specs.utils.path import e2e_test_folder_path

storage_path = os.path.join(e2e_test_folder_path(__file__), ".config", "test")


def test_register_all_hooks_correctly():
    (as_a_user(__file__).run_hexagon(["echo", "dev"]).exit())

    with open(os.path.join(storage_path, "hook_start.txt"), "r") as file:
        assert file.read() == "1"

    with open(
        os.path.join(storage_path, "hook_tool_selected-tool_name.txt"), "r"
    ) as file:
        assert file.read() == "echo"

    with open(
        os.path.join(storage_path, "hook_env_selected-env_name.txt"), "r"
    ) as file:
        assert file.read() == "dev"

    with open(
        os.path.join(storage_path, "hook_before_tool_executed-tool_name.txt"), "r"
    ) as file:
        assert file.read() == "echo"

    with open(
        os.path.join(storage_path, "hook_tool_executed-env_args.txt"), "r"
    ) as file:
        assert file.read() == "789\nghi\n"

    with open(os.path.join(storage_path, "hook_end.txt"), "r") as file:
        assert file.read() == "1"


def test_hexagon_exists_early_even_when_long_running_background_plugin():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["echo", "dev"],
            os_env_vars={"HEXAGON_TEST_PLUGIN_TEST_NAME": "async_cancel_early"},
        )
        .exit(execution_time=2)
    )


def test_hexagon_exists_on_error_even_when_long_running_background_plugin():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["error"],
            os_env_vars={"HEXAGON_TEST_PLUGIN_TEST_NAME": "async_error_early"},
        )
        .exit(1, execution_time=2)
    )

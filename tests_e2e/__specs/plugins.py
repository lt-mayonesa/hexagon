import os

from tests_e2e.__specs.utils.hexagon_spec import as_a_user
from tests_e2e.__specs.utils.path import e2e_test_folder_path

storage_path = os.path.join(e2e_test_folder_path(__file__), ".config", "test")


def test_plugins():
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

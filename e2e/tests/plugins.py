import os

from e2e.tests.utils.hexagon_spec import as_a_user
from e2e.tests.utils.path import e2e_test_folder_path

storage_path = os.path.join(e2e_test_folder_path(__file__), ".config", "test")


def test_plugins():
    (as_a_user(__file__).run_hexagon(["echo", "dev"]).exit())

    with open(os.path.join(storage_path, "started.txt"), "r") as file:
        assert file.read() == "1"

    with open(os.path.join(storage_path, "ended.txt"), "r") as file:
        assert file.read() == "1"

    with open(os.path.join(storage_path, "tool_selected.txt"), "r") as file:
        assert file.read() == "echo"

    with open(os.path.join(storage_path, "env_selected.txt"), "r") as file:
        assert file.read() == "dev"

    with open(os.path.join(storage_path, "execution_parameters.txt"), "r") as file:
        assert file.read() == "echo"

    with open(os.path.join(storage_path, "execution_data.txt"), "r") as file:
        assert file.read() == "echo"

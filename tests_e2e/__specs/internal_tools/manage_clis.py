import os
import shutil
from pathlib import Path

import pytest

from tests_e2e.__specs.utils.hexagon_spec import as_a_user, HexagonSpec
from tests_e2e.__specs.utils.path import e2e_test_folder_path

commands_dir_path = os.path.realpath(
    os.path.join(
        __file__,
        os.path.pardir,
        os.path.pardir,
        os.path.pardir,
        "internal_tools",
        "manage_clis",
        "bin",
    )
)
test_folder_path = e2e_test_folder_path(__file__)
storage_path = os.path.join(test_folder_path, "storage")

cli_install_path_storage_key = "cli-install-path"


def _delete_directory_if_exists(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)


@pytest.fixture(autouse=True)
def prepare_test():
    _delete_directory_if_exists(storage_path)
    Path(os.path.join(storage_path, "hexagon")).mkdir(exist_ok=True, parents=True)
    # Path(os.path.join(test_folder_path, "bin")).mkdir(exist_ok=True, parents=True)
    with open(
        os.path.join(storage_path, "hexagon", f"{cli_install_path_storage_key}.txt"),
        "w",
    ) as file:
        file.write(commands_dir_path)


def test_something_quick():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["manage-clis"],
            os_env_vars={
                HexagonSpec.HEXAGON_STORAGE_PATH: storage_path,
                HexagonSpec.HEXAGON_THEME: "no_border",
            },
        )
        .enter()
        # .then_output_should_be(["hola"])
        # .arrow_down()
        .enter()
        .exit()
    )

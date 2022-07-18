import shutil
from pathlib import Path

from e2e.tests.utils.path import e2e_test_folder_path
from e2e.tests.utils.hexagon_spec import as_a_user, HexagonSpec
import os

from hexagon.support.storage import HexagonStorageKeys
from hexagon.support.dependencies import (
    HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE,
)

commands_dir_path = os.path.realpath(
    os.path.join(__file__, os.path.pardir, os.path.pardir, "install_cli", "bin")
)
test_folder_path = e2e_test_folder_path(__file__)
storage_path = os.path.join(test_folder_path, "storage")


def _delete_directory_if_exists(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)


def test_install_cli():
    _delete_directory_if_exists(storage_path)
    Path(os.path.join(storage_path, "hexagon")).mkdir(exist_ok=True, parents=True)
    Path(os.path.join(test_folder_path, "bin")).mkdir(exist_ok=True, parents=True)
    with open(
        os.path.join(
            storage_path, "hexagon", f"{HexagonStorageKeys.cli_install_path.value}.txt"
        ),
        "w",
    ) as file:
        file.write(commands_dir_path)

    command = "hexagon-test"
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                HexagonSpec.HEXAGON_STORAGE_PATH: storage_path,
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE: "1",
            }
        )
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "❯",
                "",
                "Install CLI                                               Install a custom",
                "",
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ]
        )
        .enter()
        .input("/config.yml")
        .enter()
        .then_output_should_be(
            ["would have ran python3 -m pip install -r requirements.txt"], True
        )
        .then_output_should_be(["would have ran npm install --only=production"])
        .then_output_should_be(["$ hexagon-test"], True)
        .exit()
    )

    with open(os.path.join(commands_dir_path, command), "r") as file:
        assert (
            file.read() == "#!/bin/bash\n"
            "# file create by hexagon\n"
            f'HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config.yml")} hexagon $@'
        )  # noqa: E501


def test_warn_install_dir_not_PATH():
    _delete_directory_if_exists(storage_path)
    Path(os.path.join(storage_path, "hexagon")).mkdir(exist_ok=True, parents=True)
    Path(os.path.join(test_folder_path, "bin")).mkdir(exist_ok=True, parents=True)
    with open(
        os.path.join(
            storage_path, "hexagon", f"{HexagonStorageKeys.cli_install_path.value}.txt"
        ),
        "w",
    ) as file:
        file.write(commands_dir_path)

    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                HexagonSpec.HEXAGON_STORAGE_PATH: storage_path,
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE: "1",
                "HEXAGON_THEME": "default",
            }
        )
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "❯",
                "",
                "Install CLI                                               Install a custom",
                "",
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ],
            discard_until_first_match=True,
        )
        .enter()
        .input("/config.yml")
        .enter()
        .then_output_should_be(
            ["would have ran python3 -m pip install -r requirements.txt"], True
        )
        .then_output_should_be(["would have ran npm install --only=production"])
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .then_output_should_be(["", f"{commands_dir_path} is not in your $PATH"])
        .exit()
    )


def test_do_not_warn_install_dir_not_PATH_when_it_is():
    _delete_directory_if_exists(storage_path)
    Path(os.path.join(storage_path, "hexagon")).mkdir(exist_ok=True, parents=True)
    Path(os.path.join(test_folder_path, "bin")).mkdir(exist_ok=True, parents=True)
    with open(
        os.path.join(
            storage_path, "hexagon", f"{HexagonStorageKeys.cli_install_path.value}.txt"
        ),
        "w",
    ) as file:
        file.write(commands_dir_path)

    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                HexagonSpec.HEXAGON_STORAGE_PATH: storage_path,
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE: "1",
                "HEXAGON_THEME": "default",
                "PATH": f"{os.getenv('PATH')}:{commands_dir_path}",
            }
        )
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "❯",
                "",
                "Install CLI                                               Install a custom",
                "",
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ],
            discard_until_first_match=True,
        )
        .enter()
        .input("/config.yml")
        .enter()
        .then_output_should_be(
            ["would have ran python3 -m pip install -r requirements.txt"], True
        )
        .then_output_should_be(["would have ran npm install --only=production"])
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .then_output_should_not_contain([f"{commands_dir_path} is not in your $PATH"])
        .exit()
    )

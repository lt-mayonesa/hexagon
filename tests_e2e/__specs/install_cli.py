import os
import shutil
from pathlib import Path

import pytest

from tests_e2e.__specs.utils.hexagon_spec import as_a_user, HexagonSpec
from tests_e2e.__specs.utils.path import e2e_test_folder_path

commands_dir_path = os.path.realpath(
    os.path.join(__file__, os.path.pardir, os.path.pardir, "install_cli", "bin")
)
test_folder_path = e2e_test_folder_path(__file__)
storage_path = os.path.join(test_folder_path, "storage")

TEST_ENV_VARS = {
    HexagonSpec.HEXAGON_STORAGE_PATH: storage_path,
    "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
    "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
}

cli_install_path_storage_key = "cli-install-path"


def _delete_directory_if_exists(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)


@pytest.fixture(autouse=True)
def prepare_test():
    _delete_directory_if_exists(storage_path)
    Path(os.path.join(storage_path, "hexagon")).mkdir(exist_ok=True, parents=True)
    Path(os.path.join(test_folder_path, "bin")).mkdir(exist_ok=True, parents=True)
    with open(
        os.path.join(storage_path, "hexagon", f"{cli_install_path_storage_key}.txt"),
        "w",
    ) as file:
        file.write(commands_dir_path)


def test_install_cli():
    command = "hexagon-test"
    spec = (
        as_a_user(__file__)
        .run_hexagon(os_env_vars=TEST_ENV_VARS)
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "❯",
                "Install CLI                                               Install a custom",
            ]
        )
        .enter()
        .input("/config.yml")
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
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE=/private{os.path.join("/private", spec.test_dir, "config.yml")} \\\n'
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_and_provide_bins_path():
    os.remove(
        os.path.join(storage_path, "hexagon", f"{cli_install_path_storage_key}.txt")
    )

    command = "hexagon-test"
    spec = (
        as_a_user(__file__)
        .run_hexagon(os_env_vars=TEST_ENV_VARS)
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "❯",
                "Install CLI                                               Install a custom",
            ]
        )
        .enter()
        .input("/config.yml")
        .erase(str(os.path.expanduser(os.path.join("~", ".local", "bin"))))
        .input(commands_dir_path)
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
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE=/private{os.path.join(spec.test_dir, "config.yml")} \\\n'
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_pass_arguments():
    os.remove(
        os.path.join(storage_path, "hexagon", f"{cli_install_path_storage_key}.txt")
    )

    command = "hexagon-test"
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(e2e_test_folder_path(__file__), "config.yml"),
                f"--bin-path={commands_dir_path}",
            ],
            os_env_vars=TEST_ENV_VARS,
        )
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
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config.yml")} \\\n'
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_change_entrypoint_shell():
    command = "hexagon-test"
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(
                    e2e_test_folder_path(__file__), "config_entrypoint_shell.yml"
                ),
                f"--bin-path={commands_dir_path}",
            ],
            os_env_vars=TEST_ENV_VARS,
        )
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .exit()
    )

    with open(os.path.join(commands_dir_path, command), "r") as file:
        assert (
            file.read() == "#!/bin/sh\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config_entrypoint_shell.yml")} \\\n'
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_change_entrypoint_pre_command():
    command = "hexagon-test"
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(
                    e2e_test_folder_path(__file__), "config_entrypoint_pre_command.yml"
                ),
                f"--bin-path={commands_dir_path}",
            ],
            os_env_vars=TEST_ENV_VARS,
        )
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .exit()
    )

    with open(os.path.join(commands_dir_path, command), "r") as file:
        assert (
            file.read() == "#!/bin/bash\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config_entrypoint_pre_command.yml")} \\\n'
            f"pipenv run hexagon $@"
        )  # noqa: E501


def test_install_cli_change_entrypoint_environ():
    command = "hexagon-test"
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(
                    e2e_test_folder_path(__file__), "config_entrypoint_environ.yml"
                ),
                f"--bin-path={commands_dir_path}",
            ],
            os_env_vars=TEST_ENV_VARS,
        )
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .exit()
    )

    with open(os.path.join(commands_dir_path, command), "r") as file:
        assert (
            file.read() == "#!/bin/bash\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config_entrypoint_environ.yml")} \\\n'
            "MY_TEST_ENV_VAR=test \\\n"
            "ANOTHER_TEST_ENV_VAR=123 \\\n"
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_change_entrypoint_complete():
    command = "hexagon-test"
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(
                    e2e_test_folder_path(__file__), "config_entrypoint_complete.yml"
                ),
                f"--bin-path={commands_dir_path}",
            ],
            os_env_vars=TEST_ENV_VARS,
        )
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .exit()
    )

    with open(os.path.join(commands_dir_path, command), "r") as file:
        assert (
            file.read() == "#!/usr/bin/env zsh\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config_entrypoint_complete.yml")} \\\n'
            "ANOTHER_TEST_ENV_VAR=123 \\\n"
            f"poetry run hexagon $@"
        )  # noqa: E501


# noinspection PyPep8Naming
def test_warn_install_dir_not_PATH():
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                HexagonSpec.HEXAGON_STORAGE_PATH: storage_path,
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
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
        .then_output_should_be(
            ["would have ran python3 -m pip install -r requirements.txt"], True
        )
        .then_output_should_be(["would have ran npm install --only=production"])
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .then_output_should_be(
            [
                f"{commands_dir_path} is not in your $PATH",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


# noinspection PyPep8Naming
def test_do_not_warn_install_dir_not_in_PATH_when_it_is():
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                HexagonSpec.HEXAGON_STORAGE_PATH: storage_path,
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
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
        .then_output_should_be(
            ["would have ran python3 -m pip install -r requirements.txt"], True
        )
        .then_output_should_be(["would have ran npm install --only=production"])
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .then_output_should_not_contain([f"{commands_dir_path} is not in your $PATH"])
        .exit()
    )


def test_do_not_install_dependencies_when_no_custom_tools_dir_present():
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                HexagonSpec.HEXAGON_STORAGE_PATH: storage_path,
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
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
        .input("/config_no_custom_tools_dir.yml")
        .then_output_should_not_contain(
            ["would have ran npm install --only=production"]
        )
        .exit()
    )

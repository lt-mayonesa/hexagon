import os
import tempfile
from pathlib import Path

import pytest

from tests_e2e.__specs.utils.hexagon_spec import as_a_user
from tests_e2e.__specs.utils.path import e2e_test_folder_path

TEST_ENV_VARS = {
    "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
    "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
}

cli_install_path_storage_key = "cli-install-path"

test_dirs = {}


def binary_location_path(test_folder_path):
    return os.path.join(test_folder_path, "bin")


@pytest.fixture(autouse=True)
def prepare_test(request):
    test_folder_path = test_dirs.get(
        request.node.name, tempfile.mkdtemp(suffix="_hexagon")
    )
    test_dirs[request.node.name] = test_folder_path

    Path(os.path.join(test_folder_path, ".config", "hexagon")).mkdir(
        exist_ok=True, parents=True
    )
    Path(binary_location_path(test_folder_path)).mkdir(exist_ok=True, parents=True)
    with open(
        os.path.join(
            test_folder_path,
            ".config",
            "hexagon",
            f"{cli_install_path_storage_key}.txt",
        ),
        "w",
    ) as file:
        file.write(os.path.realpath(binary_location_path(test_folder_path)))


def test_install_cli(request):
    command = "hexagon-test"
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars=TEST_ENV_VARS, test_dir=test_folder_path)
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

    with open(
        os.path.join(binary_location_path(test_folder_path), command), "r"
    ) as file:
        assert (
            file.read() == "#!/bin/bash\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE=/private{os.path.join(test_folder_path, "config.yml")} \\\n'
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_and_provide_bins_path(request):
    command = "hexagon-test"
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars=TEST_ENV_VARS, test_dir=test_folder_path)
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
        .input(binary_location_path(test_folder_path))
        .then_output_should_be(
            ["would have ran python3 -m pip install -r requirements.txt"], True
        )
        .then_output_should_be(["would have ran npm install --only=production"])
        .then_output_should_be(["$ hexagon-test"], True)
        .exit()
    )

    with open(
        os.path.join(binary_location_path(test_folder_path), command), "r"
    ) as file:
        assert (
            file.read() == "#!/bin/bash\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE=/private{os.path.join(test_folder_path, "config.yml")} \\\n'
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_pass_arguments(request):
    command = "hexagon-test"
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(test_folder_path, "config.yml"),
                f"--bin-path={binary_location_path(test_folder_path)}",
            ],
            os_env_vars=TEST_ENV_VARS,
            test_dir=test_folder_path,
        )
        .then_output_should_be(
            ["would have ran python3 -m pip install -r requirements.txt"], True
        )
        .then_output_should_be(["would have ran npm install --only=production"])
        .then_output_should_be(["$ hexagon-test"], True)
        .exit()
    )

    with open(
        os.path.join(binary_location_path(test_folder_path), command), "r"
    ) as file:
        assert (
            file.read() == "#!/bin/bash\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE=/private{os.path.join(test_folder_path, "config.yml")} \\\n'
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_change_entrypoint_shell(request):
    command = "hexagon-test"
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(
                    e2e_test_folder_path(__file__), "config_entrypoint_shell.yml"
                ),
                f"--bin-path={binary_location_path(test_folder_path)}",
            ],
            os_env_vars=TEST_ENV_VARS,
            test_dir=test_folder_path,
        )
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .exit()
    )

    with open(
        os.path.join(binary_location_path(test_folder_path), command), "r"
    ) as file:
        assert (
            file.read() == "#!/bin/sh\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config_entrypoint_shell.yml")} \\\n'
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_change_entrypoint_pre_command(request):
    command = "hexagon-test"
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(test_folder_path, "config_entrypoint_pre_command.yml"),
                f"--bin-path={binary_location_path(test_folder_path)}",
            ],
            os_env_vars=TEST_ENV_VARS,
            test_dir=test_folder_path,
        )
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .exit()
    )

    with open(
        os.path.join(binary_location_path(test_folder_path), command), "r"
    ) as file:
        assert (
            file.read() == "#!/bin/bash\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE=/private{os.path.join(test_folder_path, "config_entrypoint_pre_command.yml")} \\\n'
            f"pipenv run hexagon $@"
        )  # noqa: E501


def test_install_cli_change_entrypoint_environ(request):
    command = "hexagon-test"
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(
                    e2e_test_folder_path(__file__), "config_entrypoint_environ.yml"
                ),
                f"--bin-path={binary_location_path(test_folder_path)}",
            ],
            os_env_vars=TEST_ENV_VARS,
            test_dir=test_folder_path,
        )
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .exit()
    )

    with open(
        os.path.join(binary_location_path(test_folder_path), command), "r"
    ) as file:
        assert (
            file.read() == "#!/bin/bash\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config_entrypoint_environ.yml")} \\\n'
            "MY_TEST_ENV_VAR=test \\\n"
            "ANOTHER_TEST_ENV_VAR=123 \\\n"
            f"hexagon $@"
        )  # noqa: E501


def test_install_cli_change_entrypoint_complete(request):
    command = "hexagon-test"
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(
            [
                "install",
                os.path.join(
                    e2e_test_folder_path(__file__), "config_entrypoint_complete.yml"
                ),
                f"--bin-path={binary_location_path(test_folder_path)}",
            ],
            os_env_vars=TEST_ENV_VARS,
            test_dir=test_folder_path,
        )
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .exit()
    )

    with open(
        os.path.join(binary_location_path(test_folder_path), command), "r"
    ) as file:
        assert (
            file.read() == "#!/usr/bin/env zsh\n"
            "# file created by hexagon\n"
            f'HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config_entrypoint_complete.yml")} \\\n'
            "ANOTHER_TEST_ENV_VAR=123 \\\n"
            f"poetry run hexagon $@"
        )  # noqa: E501


# noinspection PyPep8Naming
def test_warn_install_dir_not_PATH(request):
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
                "HEXAGON_THEME": "default",
            },
            test_dir=test_folder_path,
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
        .erase(str(os.path.expanduser(os.path.join("~", ".local", "bin"))))
        .input(binary_location_path(test_folder_path))
        .then_output_should_be(
            ["would have ran python3 -m pip install -r requirements.txt"], True
        )
        .then_output_should_be(["would have ran npm install --only=production"])
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .then_output_should_be(
            [
                "is not in your $PATH",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


# noinspection PyPep8Naming
def test_do_not_warn_install_dir_not_in_PATH_when_it_is(request):
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
                "HEXAGON_THEME": "default",
                "PATH": f"{os.getenv('PATH')}:/private{binary_location_path(test_folder_path)}",
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
        .erase(str(os.path.expanduser(os.path.join("~", ".local", "bin"))))
        .input(binary_location_path(test_folder_path))
        .then_output_should_be(
            ["would have ran python3 -m pip install -r requirements.txt"], True
        )
        .then_output_should_be(["would have ran npm install --only=production"])
        .then_output_should_be(["$ hexagon-test"], discard_until_first_match=True)
        .then_output_should_not_contain([f"is not in your $PATH"])
        .exit()
    )


def test_do_not_install_dependencies_when_no_custom_tools_dir_present(request):
    test_folder_path = test_dirs[request.node.name]
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
                "HEXAGON_THEME": "default",
                "PATH": f"{os.getenv('PATH')}:{binary_location_path(test_folder_path)}",
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
        .erase(str(os.path.expanduser(os.path.join("~", ".local", "bin"))))
        .input(binary_location_path(test_folder_path))
        .then_output_should_not_contain(
            ["would have ran npm install --only=production"]
        )
        .exit()
    )

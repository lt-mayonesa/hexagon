import copy

from ruamel.yaml.main import YAML
from e2e.tests.utils.hexagon_spec import as_a_user
from e2e.tests.utils.path import e2e_test_folder_path
import os
import shutil
import pytest
from pathlib import Path

storage_path = os.path.join(e2e_test_folder_path(__file__), "storage")
base_env_vars = {"HEXAGON_THEME": "result_only", "HEXAGON_STORAGE_PATH": storage_path}
local_options = {"update_time_between_checks": "2 0:00:00"}
cli_config = {
    "cli": {
        "name": "Test",
        "command": "hexagon-test",
        "custom_tools_dir": ".",
    },
    "tools": [
        {
            "name": "print-options",
            "type": "hexagon",
            "action": "get_options",
        }
    ],
    "envs": [],
}


@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists(storage_path):
        shutil.rmtree(storage_path)
    Path(storage_path).mkdir(exist_ok=True, parents=True)


def _write_local_options(options):
    file_path = os.path.join(storage_path, "hexagon", "options") + ".yaml"
    Path(os.path.dirname(file_path)).mkdir(exist_ok=True, parents=True)
    with open(file_path, "w") as file:
        YAML().dump(options, file)


def test_default_options():
    (
        as_a_user(__file__)
        .given_a_cli_yaml(cli_config)
        .run_hexagon(["print-options"], base_env_vars)
        .then_output_should_be(
            [
                "theme: result_only",
                "update_time_between_checks: 1 day, 0:00:00",
                "send_telemetry: False",
                "disable_dependency_scan: True",
                "update_disabled: True",
                "cli_update_disabled: True",
                "config_storage_path: None",
            ],
            True,
        )
        .exit()
    )


def test_local_options():
    _write_local_options(local_options)

    (
        as_a_user(__file__)
        .given_a_cli_yaml(cli_config)
        .run_hexagon(["print-options"], base_env_vars)
        .then_output_should_be(
            [
                "theme: result_only",
                "update_time_between_checks: 2 days, 0:00:00",
                "send_telemetry: False",
                "disable_dependency_scan: True",
                "update_disabled: True",
                "cli_update_disabled: True",
                "config_storage_path: None",
            ],
        )
        .exit()
    )


def test_env_variable():
    _write_local_options(local_options)

    (
        as_a_user(__file__)
        .given_a_cli_yaml(cli_config)
        .run_hexagon(
            ["print-options"],
            {**base_env_vars, "HEXAGON_UPDATE_TIME_BETWEEN_CHECKS": "3 0:00:00"},
        )
        .then_output_should_be(["update_time_between_checks: 3 days, 0:00:00"], True)
        .exit()
    )


def test_options_in_configuration_file():
    _write_local_options(local_options)

    app = copy.deepcopy(cli_config)
    app["cli"]["options"] = {"update_time_between_checks": "23 0:00:00"}

    (
        as_a_user(__file__)
        .given_a_cli_yaml(app)
        .run_hexagon(
            ["print-options"],
            {**base_env_vars, "HEXAGON_UPDATE_TIME_BETWEEN_CHECKS": "3 0:00:00"},
        )
        .then_output_should_be(["update_time_between_checks: 23 days, 0:00:00"], True)
        .exit()
    )


def test_invalid_local_options():
    _write_local_options({"update_time_between_checks": "SARLANGA"})

    (
        as_a_user(__file__)
        .given_a_cli_yaml(cli_config)
        .run_hexagon(["print-options"], base_env_vars)
        .then_output_should_be(
            [
                "There were 1 error(s) in your YAML",
                "",
                "✗ update_time_between_checks -> invalid duration format",
            ]
        )
        .exit(1)
    )

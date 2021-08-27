from ruamel.yaml.main import YAML
from hexagon.support.storage import HEXAGON_STORAGE_APP, HexagonStorageKeys
from e2e.tests.utils.hexagon_spec import as_a_user
from e2e.tests.utils.path import e2e_test_folder_path
import os
import shutil
import pytest
from pathlib import Path

storage_path = os.path.join(e2e_test_folder_path(__file__), "storage")
base_env_vars = {"HEXAGON_THEME": "default", "HEXAGON_STORAGE_PATH": storage_path}
local_options = {"update_time_between_checks": "2 0:00:00"}


@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists(storage_path):
        shutil.rmtree(storage_path)
    Path(storage_path).mkdir(exist_ok=True, parents=True)


def _write_local_options(options):
    file_path = (
        os.path.join(
            storage_path, HEXAGON_STORAGE_APP, HexagonStorageKeys.options.value
        )
        + ".yaml"
    )
    Path(os.path.dirname(file_path)).mkdir(exist_ok=True, parents=True)
    with open(file_path, "w") as file:
        YAML().dump(options, file)


def test_default_options():
    (
        as_a_user(__file__)
        .run_hexagon(["print-options"], base_env_vars)
        .then_output_should_be(["update_time_between_checks: 1 day, 0:00:00"], True)
        .exit()
    )


def test_local_options():
    _write_local_options(local_options)

    (
        as_a_user(__file__)
        .run_hexagon(["print-options"], base_env_vars)
        .then_output_should_be(["update_time_between_checks: 2 days, 0:00:00"], True)
        .exit()
    )


def test_env_variable():
    _write_local_options(local_options)

    (
        as_a_user(__file__)
        .run_hexagon(
            ["print-options"],
            {**base_env_vars, "HEXAGON_UPDATE_TIME_BETWEEN_CHECKS": "3 0:00:00"},
        )
        .then_output_should_be(["update_time_between_checks: 3 days, 0:00:00"], True)
        .exit()
    )


def test_invalid_local_options():
    _write_local_options({"update_time_between_checks": "SARLANGA"})

    (
        as_a_user(__file__)
        .run_hexagon(
            ["print-options"],
            base_env_vars,
        )
        .then_output_should_be(
            [
                "There were 1 error(s) in your YAML",
                "",
                "✗ update_time_between_checks -> invalid duration format",
            ]
        )
        .exit(1)
    )

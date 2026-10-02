import copy
import os
from pathlib import Path

from ruamel.yaml.main import YAML

from tests_e2e.framework.hexagon_spec import as_a_user

base_env_vars = {"HEXAGON_THEME": "result_only"}
local_options = {"update_time_between_checks": "P2D"}
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


def _write_local_options(test_dir, options):
    file_path = os.path.join(test_dir, ".config", "hexagon", "options") + ".yaml"
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
    (
        as_a_user(__file__)
        .executing_first(
            lambda spec: _write_local_options(spec.test_dir, local_options)
        )
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
    (
        as_a_user(__file__)
        .executing_first(
            lambda spec: _write_local_options(spec.test_dir, local_options)
        )
        .given_a_cli_yaml(cli_config)
        .run_hexagon(
            ["print-options"],
            {**base_env_vars, "HEXAGON_UPDATE_TIME_BETWEEN_CHECKS": "P3D"},
        )
        .then_output_should_be(["update_time_between_checks: 3 days, 0:00:00"], True)
        .exit()
    )


def test_options_in_configuration_file():
    """
    Given app.yml has cli.options with update_time_between_checks=P23D
    When no envvar or cli_options.yml overrides the value
    Then app.yml options are applied.
    """
    app = copy.deepcopy(cli_config)
    app["cli"]["options"] = {"update_time_between_checks": "P23D"}

    (
        as_a_user(__file__)
        .given_a_cli_yaml(app)
        .run_hexagon(["print-options"], base_env_vars)
        .then_output_should_be(["update_time_between_checks: 23 days, 0:00:00"], True)
        .exit()
    )


def test_envvar_overrides_configuration_file():
    """
    Given app.yml has cli.options with update_time_between_checks=P23D
    And an envvar HEXAGON_UPDATE_TIME_BETWEEN_CHECKS=P3D is set
    Then envvar wins (priority: envvars > cli_options.yml > app.yml options).
    """
    app = copy.deepcopy(cli_config)
    app["cli"]["options"] = {"update_time_between_checks": "P23D"}

    (
        as_a_user(__file__)
        .given_a_cli_yaml(app)
        .run_hexagon(
            ["print-options"],
            {**base_env_vars, "HEXAGON_UPDATE_TIME_BETWEEN_CHECKS": "P3D"},
        )
        .then_output_should_be(["update_time_between_checks: 3 days, 0:00:00"], True)
        .exit()
    )


def _write_cli_options_yml(test_dir, options):
    file_path = os.path.join(test_dir, "cli_options.yml")
    with open(file_path, "w") as f:
        YAML().dump(options, f)


def test_cli_options_yml_is_loaded():
    """
    Given a cli_options.yml file exists next to app.yml
    When hexagon runs
    Then options from cli_options.yml are applied.
    """
    (
        as_a_user(__file__)
        .executing_first(
            lambda spec: _write_cli_options_yml(
                spec.test_dir, {"update_time_between_checks": "P7D"}
            )
        )
        .given_a_cli_yaml(cli_config)
        .run_hexagon(["print-options"], base_env_vars)
        .then_output_should_be(["update_time_between_checks: 7 days, 0:00:00"], True)
        .exit()
    )


def test_cli_options_yml_overrides_app_yml_options():
    """
    Given app.yml has cli.options with update_time_between_checks=P23D
    And cli_options.yml has update_time_between_checks=P7D
    Then cli_options.yml wins over app.yml options.
    """
    app = copy.deepcopy(cli_config)
    app["cli"]["options"] = {"update_time_between_checks": "P23D"}

    (
        as_a_user(__file__)
        .executing_first(
            lambda spec: _write_cli_options_yml(
                spec.test_dir, {"update_time_between_checks": "P7D"}
            )
        )
        .given_a_cli_yaml(app)
        .run_hexagon(["print-options"], base_env_vars)
        .then_output_should_be(["update_time_between_checks: 7 days, 0:00:00"], True)
        .exit()
    )


def test_envvar_overrides_cli_options_yml():
    """
    Given cli_options.yml has update_time_between_checks=P7D
    And envvar HEXAGON_UPDATE_TIME_BETWEEN_CHECKS=P3D is set
    Then envvar wins (highest priority).
    """
    (
        as_a_user(__file__)
        .executing_first(
            lambda spec: _write_cli_options_yml(
                spec.test_dir, {"update_time_between_checks": "P7D"}
            )
        )
        .given_a_cli_yaml(cli_config)
        .run_hexagon(
            ["print-options"],
            {**base_env_vars, "HEXAGON_UPDATE_TIME_BETWEEN_CHECKS": "P3D"},
        )
        .then_output_should_be(["update_time_between_checks: 3 days, 0:00:00"], True)
        .exit()
    )


def test_invalid_local_options():
    (
        as_a_user(__file__)
        .executing_first(
            lambda spec: _write_local_options(
                spec.test_dir, {"update_time_between_checks": "SARLANGA"}
            )
        )
        .given_a_cli_yaml(cli_config)
        .run_hexagon(["print-options"], base_env_vars)
        .then_output_should_be(
            [
                "There were 1 error(s) in your YAML",
                "",
                "✗ update_time_between_checks -> Input should be a valid timedelta, invalid character in hour",
            ],
            ignore_blank_lines=False,
        )
        .exit(1)
    )

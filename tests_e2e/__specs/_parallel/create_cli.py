import os

from tests_e2e.framework.config import read_hexagon_config
from tests_e2e.framework.hexagon_spec import HexagonSpec, as_a_user

# Test data
CLI_DIR_NAME = "my-team-tools"
CLI_TITLE = "My Team CLI"
CLI_COMMAND = "mt"

base_app_file = {
    "cli": {"name": "Test", "command": "hexagon-test"},
    "tools": [],
    "envs": [],
}


def _shared_assertions(spec: HexagonSpec):
    """
    Shared assertions for create_cli tests.
    """
    (
        spec.then_output_should_be(
            ["Hi, which tool would you like to use today?"],
            discard_until_first_match=True,
        )
        .arrow_down()  # Navigate to 'Create A New CLI Project'
        .enter()
        .then_output_should_be(
            [
                [
                    "Hi, which tool would you like to use today?",
                    "Create A New CLI Project",
                ]
            ],
            discard_until_first_match=True,
        )
    )


def test_create_cli_basic():
    """
    Given a user wants to create a new CLI project
    When they run the create CLI tool and provide all required information
    Then a new CLI project is created with the correct structure
    """
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .with_shared_behavior(_shared_assertions)
        .input(CLI_DIR_NAME)
        .then_output_should_be(
            [["Enter the directory name for your CLI project:", CLI_DIR_NAME]],
            discard_until_first_match=True,
        )
        .input(CLI_TITLE)
        .then_output_should_be(
            [["Enter a title for your CLI:", CLI_TITLE]],
            discard_until_first_match=True,
        )
        .erase(CLI_DIR_NAME)
        .input(CLI_COMMAND)
        .then_output_should_be(
            [["Enter the command to execute your CLI:", CLI_COMMAND]],
            discard_until_first_match=True,
        )
        .input("dev")
        .input("prod-eu")
        .input("prod-us")
        .esc()
        .carriage_return()
        .then_output_should_be(
            [["Enter your environments:", "dev..."]],
            discard_until_first_match=True,
        )
        .exit()
    )

    # Verify the CLI project was created correctly
    cli_dir_path = os.path.join(spec.test_dir, CLI_DIR_NAME)
    app_yml_path = os.path.join(cli_dir_path, "app.yml")

    # Check that the directory and files exist
    assert os.path.isdir(cli_dir_path), f"CLI directory {cli_dir_path} was not created"
    assert os.path.isfile(app_yml_path), f"app.yml file {app_yml_path} was not created"

    # Check the content of app.yml
    app_file = read_hexagon_config(cli_dir_path)
    assert (
        app_file["cli"]["name"] == CLI_TITLE
    ), f"CLI title does not match: {app_file['cli']['title']} != {CLI_TITLE}"
    assert (
        app_file["cli"]["command"] == CLI_COMMAND
    ), f"CLI command does not match: {app_file['cli']['command']} != {CLI_COMMAND}"

    # Check environments
    expected_envs = [
        {"name": "dev", "alias": "d"},
        {"name": "prod-eu", "alias": "pe"},
        {"name": "prod-us", "alias": "pu"},
    ]

    assert len(app_file["envs"]) == len(
        expected_envs
    ), f"Expected {len(expected_envs)} environments, got {len(app_file['envs'])}"

    for i, expected_env in enumerate(expected_envs):
        actual_env = app_file["envs"][i]
        assert (
            actual_env["name"] == expected_env["name"]
        ), f"Environment name does not match: {actual_env['name']} != {expected_env['name']}"
        assert (
            actual_env["alias"] == expected_env["alias"]
        ), f"Environment alias does not match: {actual_env['alias']} != {expected_env['alias']}"

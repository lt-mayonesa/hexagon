import os
import tempfile
from datetime import date, timedelta
from pathlib import Path

from __specs.utils.path import e2e_test_folder_path
from tests_e2e.__specs.utils.hexagon_spec import as_a_user

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"


def _write_last_check(test_dir, last_check_date):
    Path(os.path.join(test_dir, ".config", "hexagon")).mkdir(
        exist_ok=True, parents=True
    )
    with open(
        os.path.join(test_dir, ".config", "hexagon", "last-update-check.txt"), "w"
    ) as file:
        file.write(last_check_date.strftime(LAST_UPDATE_DATE_FORMAT))


temp_file_path = os.path.join(e2e_test_folder_path(__file__), "pypi_version_mock.json")

base_os_env_vars = {
    "HEXAGON_UPDATE_DISABLED": "false",
    "HEXAGON_TEST_LOCAL_VERSION_OVERRIDE": "0.1.0",
    "HEXAGON_TEST_LATEST_VERSION_OVERRIDE": f"file://{temp_file_path}",
}

no_changelog_env_vars = {**base_os_env_vars, "HEXAGON_UPDATE_SHOW_CHANGELOG": ""}


def test_new_hexagon_version_available():
    (
        as_a_user(__file__)
        .run_hexagon(["my-module"], os_env_vars=no_changelog_env_vars)
        .write("n")
        .then_output_should_be(
            [["Would you like to update?", "No"]], discard_until_first_match=True
        )
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_prompt_to_update_hexagon_only_once():
    spec = (
        as_a_user(__file__)
        .run_hexagon(["my-module"], os_env_vars=no_changelog_env_vars)
        .write("n")
        .then_output_should_be(
            [["Would you like to update?", "No"]], discard_until_first_match=True
        )
        .then_output_should_be(["my-module"])
        .exit()
    )

    (
        as_a_user(__file__)
        .run_hexagon(
            ["my-module"], os_env_vars=no_changelog_env_vars, test_dir=spec.test_dir
        )
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_prompt_to_update_hexagon_once_a_day():
    test_folder_path = tempfile.mkdtemp(suffix="_hexagon")
    _write_last_check(test_folder_path, date.today())

    (
        as_a_user(__file__)
        .run_hexagon(
            ["my-module"], os_env_vars=no_changelog_env_vars, test_dir=test_folder_path
        )
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_prompt_to_update_hexagon_again_next_day():
    test_folder_path = tempfile.mkdtemp(suffix="_hexagon")
    _write_last_check(test_folder_path, date.today() - timedelta(days=1))

    (
        as_a_user(__file__)
        .run_hexagon(
            ["my-module"], os_env_vars=no_changelog_env_vars, test_dir=test_folder_path
        )
        .write("n")
        .then_output_should_be(
            [["Would you like to update?", "No"]], discard_until_first_match=True
        )
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_show_changelog():
    test_folder_path = tempfile.mkdtemp(suffix="_hexagon")
    (
        as_a_user(__file__)
        .run_hexagon(
            ["my-module"],
            os_env_vars={
                **base_os_env_vars,
                "HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE": os.path.join(
                    test_folder_path, "CHANGELOG.md"
                ),
                "HEXAGON_TEST_LOCAL_VERSION_OVERRIDE": "0.59.0",
                "HEXAGON_THEME": "default",
            },
            test_dir=test_folder_path,
        )
        .then_output_should_be(["New hexagon version available"], True)
        .then_output_should_be(
            [
                "## v0.61.0",
                "### release",
                "chore: specify build command",
                "chore: configure semantic release v9",
                "### ci",
                "chore: publish to PyPi",
                "### deps",
                "chore: bump actions/checkout from 3 to 4",
                "chore: bump nick-fields/retry from 2 to 3",
                "chore: bump actions/setup-python from 4 to 5",
                "chore: bump markdown from 3.6 to 3.7",
                "## v0.60.0",
                "### deps",
                "chore: setup dependabot version upgrades",
                "chore: migrate to pydantic v2 (#81)",
                "### prompt",
                "feat: allow to provide text suggestions (#88)",
            ],
            True,
        )
        .write("n")
        .then_output_should_be(
            [["Would you like to update?", "No"]],
            discard_until_first_match=True,
        )
        .then_output_should_be(["my-module"])
        .exit()
    )

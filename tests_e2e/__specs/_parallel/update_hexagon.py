import os
from datetime import date, timedelta
from pathlib import Path

from tests_e2e.framework.hexagon_spec import as_a_user

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"


def _write_last_check(test_dir, last_check_date):
    Path(os.path.join(test_dir, ".config", "hexagon")).mkdir(
        exist_ok=True, parents=True
    )
    with open(
        os.path.join(test_dir, ".config", "hexagon", "last-update-check.txt"), "w"
    ) as file:
        file.write(last_check_date.strftime(LAST_UPDATE_DATE_FORMAT))


def base_os_env_vars(test_dir):
    return {
        "HEXAGON_UPDATE_DISABLED": "false",
        "HEXAGON_TEST_LOCAL_VERSION_OVERRIDE": "0.1.0",
        "HEXAGON_TEST_LATEST_VERSION_OVERRIDE": f"file://{os.path.join(test_dir, 'pypi_version_mock.json')}",
    }


def no_changelog_env_vars(test_dir):
    return {**base_os_env_vars(test_dir), "HEXAGON_UPDATE_SHOW_CHANGELOG": ""}


def test_new_hexagon_version_available():
    spec = as_a_user(__file__)
    (
        spec.run_hexagon(
            ["my-module"], os_env_vars=no_changelog_env_vars(spec.test_dir)
        )
        .write("n")
        .then_output_should_be(
            [["Would you like to update?", "No"]], discard_until_first_match=True
        )
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_prompt_to_update_hexagon_only_once():
    spec = as_a_user(__file__)
    (
        spec.run_hexagon(
            ["my-module"], os_env_vars=no_changelog_env_vars(spec.test_dir)
        )
        .write("n")
        .then_output_should_be(
            [["Would you like to update?", "No"]], discard_until_first_match=True
        )
        .then_output_should_be(["my-module"])
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["my-module"], os_env_vars=no_changelog_env_vars(spec.test_dir))
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_prompt_to_update_hexagon_once_a_day():
    spec = as_a_user(__file__)
    _write_last_check(spec.test_dir, date.today())

    (
        spec.run_hexagon(
            ["my-module"], os_env_vars=no_changelog_env_vars(spec.test_dir)
        )
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_prompt_to_update_hexagon_again_next_day():
    spec = as_a_user(__file__)
    _write_last_check(spec.test_dir, date.today() - timedelta(days=1))

    (
        spec.run_hexagon(
            ["my-module"], os_env_vars=no_changelog_env_vars(spec.test_dir)
        )
        .write("n")
        .then_output_should_be(
            [["Would you like to update?", "No"]], discard_until_first_match=True
        )
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_show_changelog():
    spec = as_a_user(__file__)
    (
        spec.run_hexagon(
            ["my-module"],
            os_env_vars={
                **base_os_env_vars(spec.test_dir),
                "HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE": os.path.join(
                    spec.test_dir, "CHANGELOG.md"
                ),
                "HEXAGON_TEST_LOCAL_VERSION_OVERRIDE": "0.59.0",
                "HEXAGON_THEME": "default",
            },
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

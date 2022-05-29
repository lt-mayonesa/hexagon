from e2e.tests.utils.path import e2e_test_folder_path
import os
from datetime import date, timedelta
from e2e.tests.utils.hexagon_spec import as_a_user

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"

test_folder_path = e2e_test_folder_path(__file__)
storage_path = os.path.realpath(os.path.join(test_folder_path, "storage"))
last_checked_storage_path = os.path.join(
    storage_path, "hexagon", "last-update-check.txt"
)


def _write_storage_path():
    if not os.path.exists(os.path.dirname(last_checked_storage_path)):
        os.makedirs(os.path.dirname(last_checked_storage_path))


def _write_last_check(last_check_date):
    _write_storage_path()

    with open(last_checked_storage_path, "w") as file:
        file.write(last_check_date.strftime(LAST_UPDATE_DATE_FORMAT))


def _clear_last_check():
    _write_storage_path()
    if os.path.exists(last_checked_storage_path):
        os.remove(last_checked_storage_path)


base_os_env_vars = {
    "HEXAGON_UPDATE_DISABLED": "",
    "HEXAGON_TEST_VERSION_OVERRIDE": "0.1.0",
    "HEXAGON_STORAGE_PATH": storage_path,
}

no_changelog_env_vars = {**base_os_env_vars, "HEXAGON_UPDATE_SHOW_CHANGELOG": ""}


def test_new_hexagon_version_available():
    _clear_last_check()

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
    _clear_last_check()

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

    (
        as_a_user(__file__)
        .run_hexagon(["my-module"], os_env_vars=no_changelog_env_vars)
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_prompt_to_update_hexagon_once_a_day():
    _write_last_check(date.today())

    (
        as_a_user(__file__)
        .run_hexagon(["my-module"], os_env_vars=no_changelog_env_vars)
        .then_output_should_be(["my-module"])
        .exit()
    )


def test_prompt_to_update_hexagon_again_next_day():
    _write_last_check(date.today() - timedelta(days=1))

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


def test_show_changelog():
    _clear_last_check()

    (
        as_a_user(__file__)
        .run_hexagon(
            ["my-module"],
            os_env_vars={
                **base_os_env_vars,
                "HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE": os.path.join(
                    test_folder_path, "CHANGELOG.md"
                ),
                "HEXAGON_THEME": "default",
            },
        )
        .then_output_should_be(["New hexagon version available"], True)
        .then_output_should_be(
            [
                "- Feature 1",
                "- Feature 2",
                "- Feature 3",
                "- Feature 4",
                "- Fix 1",
                "- Fix 2",
                "- Fix 3",
                "- Fix 4",
                "- Documentation 1",
                "- Documentation 2",
                "and much more!",
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

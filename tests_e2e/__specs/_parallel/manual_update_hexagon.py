import os
from datetime import date
from pathlib import Path

from tests_e2e.framework.hexagon_spec import as_a_user

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"


def _write_last_check(test_dir):
    """Write last check date to simulate a previous update check."""
    Path(os.path.join(test_dir, ".config", "hexagon")).mkdir(
        exist_ok=True, parents=True
    )
    with open(
        os.path.join(test_dir, ".config", "hexagon", "last-update-check.txt"), "w"
    ) as file:
        file.write(date.today().strftime(LAST_UPDATE_DATE_FORMAT))


def base_os_env_vars(test_dir):
    return {
        "HEXAGON_UPDATE_DISABLED": "true",  # Disable automatic updates
        "HEXAGON_TEST_LOCAL_VERSION_OVERRIDE": "0.1.0",
        "HEXAGON_TEST_LATEST_VERSION_OVERRIDE": f"file://{os.path.join(test_dir, 'pypi_version_mock.json')}",
        "HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE": os.path.join(
            test_dir, "CHANGELOG.md"
        ),
        "HEXAGON_THEME": "default",
    }


def test_manual_update_hexagon_when_update_available():
    """
    Given a new hexagon version is available.
    When the user runs the update-hexagon tool.
    Then the changelog is shown and user is prompted to confirm update.
    """
    spec = as_a_user(__file__)
    (
        spec.run_hexagon(
            ["update-hexagon"], os_env_vars=base_os_env_vars(spec.test_dir)
        )
        .then_output_should_be(
            ["New hexagon version available 0.61.0"], discard_until_first_match=True
        )
        .then_output_should_be(["## v0.61.0"], discard_until_first_match=True)
        .then_output_should_be(
            ["Would you like to update?"], discard_until_first_match=True
        )
        .write("n")
        .then_output_should_be(["Update cancelled"], discard_until_first_match=True)
        .exit()
    )


def test_manual_update_hexagon_when_already_latest():
    """
    Given the user is already on the latest hexagon version.
    When the user runs the update-hexagon tool.
    Then a message is shown indicating they're on the latest version.
    """
    spec = as_a_user(__file__)
    env_vars = {
        **base_os_env_vars(spec.test_dir),
        "HEXAGON_TEST_LOCAL_VERSION_OVERRIDE": "0.61.0",  # Same as latest
    }
    (
        spec.run_hexagon(["update-hexagon"], os_env_vars=env_vars)
        .then_output_should_be(["already up to date"], discard_until_first_match=True)
        .exit()
    )


def test_manual_update_bypasses_throttle():
    """
    Given the user checked for updates today (automatic update would be throttled).
    When the user manually runs update-hexagon.
    Then the check is performed anyway (bypasses throttle).
    """
    spec = as_a_user(__file__)

    # Simulate that we already checked for updates today
    _write_last_check(spec.test_dir)

    # Manual update should bypass throttle and check anyway
    (
        spec.run_hexagon(
            ["update-hexagon"], os_env_vars=base_os_env_vars(spec.test_dir)
        )
        .then_output_should_be(
            ["New hexagon version available"], discard_until_first_match=True
        )
        .write("n")
        .exit()
    )

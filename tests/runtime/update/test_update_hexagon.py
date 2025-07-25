import os
import subprocess
import sys
from unittest import mock

from packaging.version import Version

from hexagon.runtime.update import version
from hexagon.runtime.update.hexagon import check_for_hexagon_updates
from hexagon.support.input.prompt import prompt
from hexagon.support.storage import (
    HEXAGON_STORAGE_APP,
    HexagonStorageKeys,
    delete_user_data,
)


def _confirm_mock(_, default=None):
    class ConfirmMock:
        @staticmethod
        def execute():
            return True

    return ConfirmMock()


def _local_version_mock(override=None):
    return Version("0.1.0")


def _latest_version_mock(override=None):
    return Version("0.2.0")


def test_check_for_hexagon_updates_performs_update_when_newer_version_is_available(
    monkeypatch,
):
    """
    Given:
      - Local version number is '0.1.0'.
      - Latest version number is '0.2.0'.
      - User confirms the update prompt.
      - Last update check data is deleted.
    When check_for_hexagon_updates is called.
    Then:
      - subprocess.check_call should be called once to perform the update.
      - sys.exit should be called once with exit code 1.
    """
    monkeypatch.setenv("HEXAGON_TEST_LOCAL_VERSION_OVERRIDE", "0.1.0")
    monkeypatch.setenv(
        "HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE",
        os.path.join(os.path.dirname(__file__), "TEST_CHANGELOG.md"),
    )
    monkeypatch.setattr(prompt, "confirm", _confirm_mock)
    monkeypatch.setattr(version, "local", _local_version_mock)
    monkeypatch.setattr(version, "latest", _latest_version_mock)

    delete_user_data(HEXAGON_STORAGE_APP, HexagonStorageKeys.last_update_check.value)
    with mock.patch.object(
        subprocess, "check_call"
    ) as suprocess_mock, mock.patch.object(sys, "exit") as exit_mock:
        check_for_hexagon_updates()
        suprocess_mock.assert_called_once()
        exit_mock.assert_called_once_with(1)
    delete_user_data(HEXAGON_STORAGE_APP, HexagonStorageKeys.last_update_check.value)

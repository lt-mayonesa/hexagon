import sys
import pkg_resources
from unittest import mock
import subprocess
from InquirerPy import inquirer

from hexagon.support.update.hexagon import check_for_hexagon_updates
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


def _require_mock(_, default=None):
    class PackageMock:
        version = "0.1.0"

    return [PackageMock()]


def test_hexagon_updates_itself(monkeypatch):
    monkeypatch.setenv("HEXAGON_TEST_VERSION_OVERRIDE", "0.1.0")
    monkeypatch.setattr(inquirer, "confirm", _confirm_mock)
    monkeypatch.setattr(pkg_resources, "require", _require_mock)

    delete_user_data(HEXAGON_STORAGE_APP, HexagonStorageKeys.last_update_check.value)
    with mock.patch.object(
        subprocess, "check_call"
    ) as suprocess_mock, mock.patch.object(sys, "exit") as exit_mock:
        check_for_hexagon_updates()
        suprocess_mock.assert_called_once()
        exit_mock.assert_called_once_with(1)
    delete_user_data(HEXAGON_STORAGE_APP, HexagonStorageKeys.last_update_check.value)

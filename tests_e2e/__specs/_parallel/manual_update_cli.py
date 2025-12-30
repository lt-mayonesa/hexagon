import os
import shutil
import subprocess
from datetime import date
from pathlib import Path

from tests_e2e.framework.hexagon_spec import as_a_user

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"


def _write_last_cli_check(test_dir):
    """Write last CLI check date to simulate a previous update check."""
    Path(os.path.join(test_dir, "local", ".config", "hexagon")).mkdir(
        exist_ok=True, parents=True
    )
    with open(
        os.path.join(
            test_dir, "local", ".config", "hexagon", "last-cli-update-check.txt"
        ),
        "w",
    ) as file:
        file.write(date.today().strftime(LAST_UPDATE_DATE_FORMAT))


def os_env_vars(test_folder_path):
    return {
        "HEXAGON_CLI_UPDATE_DISABLED": "true",  # Disable automatic updates
        "HEXAGON_THEME": "default",
        "PIPENV_PIPFILE": os.path.realpath(
            os.path.join(test_folder_path, os.path.pardir, os.path.pardir, "Pipfile")
        ),
    }


def _prepare(test_folder_path):
    remote_repo_path = os.path.join(test_folder_path, "remote")
    local_repo_path = os.path.join(test_folder_path, "local")
    os.makedirs(remote_repo_path, exist_ok=True)
    os.makedirs(local_repo_path, exist_ok=True)
    subprocess.check_call("git init -b main", cwd=remote_repo_path, shell=True)
    subprocess.check_call("git branch -m main", cwd=remote_repo_path, shell=True)
    files_to_copy = ["app.yml", "package.json", "Pipfile", "yarn.lock"]
    for file in files_to_copy:
        shutil.copyfile(
            os.path.join(test_folder_path, file),
            os.path.join(remote_repo_path, file),
        )

    subprocess.check_call("git add .", cwd=remote_repo_path, shell=True)
    subprocess.check_call(
        "git -c user.name='Jhon Doe' -c user.email='my@email.org' commit -m initial",
        cwd=remote_repo_path,
        shell=True,
    )
    subprocess.check_call("git clone -l remote local", cwd=test_folder_path, shell=True)


def test_manual_update_cli_when_no_changes():
    """
    Given the CLI has no pending changes.
    When the user manually runs update-cli.
    Then a message is shown indicating they're on the latest version.
    """
    spec = as_a_user(__file__)

    _prepare(spec.test_dir)

    (
        spec.run_hexagon(
            ["update-cli"],
            os_env_vars(spec.test_dir),
            test_dir=os.path.join(spec.test_dir, "local"),
        )
        .then_output_should_be(["already up to date"], discard_until_first_match=True)
        .exit()
    )


def test_manual_update_cli_when_changes_available():
    """
    Given the CLI has pending changes in git.
    When the user manually runs update-cli.
    Then the user is prompted to confirm and the update is performed.
    """
    spec = as_a_user(__file__)

    _prepare(spec.test_dir)
    remote_repo_path = os.path.join(spec.test_dir, "remote")
    shutil.copyfile(
        os.path.join(spec.test_dir, "modified-app.yml"),
        os.path.join(remote_repo_path, "app.yml"),
    )

    subprocess.check_call("git add .", cwd=remote_repo_path, shell=True)
    subprocess.check_call(
        "git -c user.name='Jhon Doe' -c user.email='my@email.org' commit -m modified",
        cwd=remote_repo_path,
        shell=True,
    )

    (
        spec.run_hexagon(
            ["update-cli"],
            {
                **os_env_vars(spec.test_dir),
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
            },
            test_dir=os.path.join(spec.test_dir, "local"),
        )
        .then_output_should_be(
            ["New Test version available"], discard_until_first_match=True
        )
        .then_output_should_be(
            ["Would you like to update?"], discard_until_first_match=True
        )
        .write("y")
        .then_output_should_be(
            ["Updated to latest version"], discard_until_first_match=True
        )
        .exit()
    )


def test_manual_update_cli_user_cancels():
    """
    Given the CLI has pending changes.
    When the user manually runs update-cli and cancels.
    Then the update is cancelled.
    """
    spec = as_a_user(__file__)

    _prepare(spec.test_dir)
    remote_repo_path = os.path.join(spec.test_dir, "remote")
    shutil.copyfile(
        os.path.join(spec.test_dir, "modified-app.yml"),
        os.path.join(remote_repo_path, "app.yml"),
    )

    subprocess.check_call("git add .", cwd=remote_repo_path, shell=True)
    subprocess.check_call(
        "git -c user.name='Jhon Doe' -c user.email='my@email.org' commit -m modified",
        cwd=remote_repo_path,
        shell=True,
    )

    (
        spec.run_hexagon(
            ["update-cli"],
            os_env_vars(spec.test_dir),
            test_dir=os.path.join(spec.test_dir, "local"),
        )
        .then_output_should_be(
            ["New Test version available"], discard_until_first_match=True
        )
        .then_output_should_be(
            ["Would you like to update?"], discard_until_first_match=True
        )
        .write("n")
        .then_output_should_be(["Update cancelled"], discard_until_first_match=True)
        .exit()
    )


def test_manual_update_cli_when_not_git_repository():
    """
    Given the CLI is not in a git repository.
    When the user manually runs update-cli.
    Then an error message is shown.
    """
    spec = as_a_user(__file__)
    local_repo_path = os.path.join(spec.test_dir, "local")
    os.makedirs(local_repo_path, exist_ok=True)

    shutil.copyfile(
        os.path.join(spec.test_dir, "app.yml"),
        os.path.join(local_repo_path, "app.yml"),
    )

    (
        spec.run_hexagon(
            ["update-cli"],
            os_env_vars(spec.test_dir),
            test_dir=local_repo_path,
        )
        .then_output_should_be(
            ["not in a git repository"], discard_until_first_match=True
        )
        .exit()
    )


def test_manual_update_cli_bypasses_throttle():
    """
    Given the user checked for CLI updates today (automatic would be throttled).
    When the user manually runs update-cli.
    Then the check is performed anyway (bypasses throttle).
    """
    spec = as_a_user(__file__)

    _prepare(spec.test_dir)
    remote_repo_path = os.path.join(spec.test_dir, "remote")
    shutil.copyfile(
        os.path.join(spec.test_dir, "modified-app.yml"),
        os.path.join(remote_repo_path, "app.yml"),
    )

    subprocess.check_call("git add .", cwd=remote_repo_path, shell=True)
    subprocess.check_call(
        "git -c user.name='Jhon Doe' -c user.email='my@email.org' commit -m modified",
        cwd=remote_repo_path,
        shell=True,
    )

    # Simulate that we already checked for CLI updates today
    _write_last_cli_check(spec.test_dir)

    # Manual update should bypass throttle and check anyway
    (
        spec.run_hexagon(
            ["update-cli"],
            os_env_vars(spec.test_dir),
            test_dir=os.path.join(spec.test_dir, "local"),
        )
        .then_output_should_be(
            ["New Test version available"], discard_until_first_match=True
        )
        .write("n")
        .exit()
    )

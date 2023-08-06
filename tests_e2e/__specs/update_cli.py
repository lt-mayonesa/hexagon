import os
import shutil
import subprocess
import tempfile

from tests_e2e.__specs.utils.hexagon_spec import as_a_user
from tests_e2e.__specs.utils.path import e2e_test_folder_path

test_folder_path = e2e_test_folder_path(__file__)
storage_path = os.path.join(test_folder_path, "storage")
local_repo_path = os.path.join(test_folder_path, "local")
remote_repo_path = os.path.join(test_folder_path, "remote")

last_checked_storage_path = os.path.join(storage_path, "test", "last-update-check.txt")

os_env_vars = {
    "HEXAGON_STORAGE_PATH": storage_path,
    "HEXAGON_CLI_UPDATE_DISABLED": "false",
    "PIPENV_PIPFILE": os.path.realpath(
        os.path.join(test_folder_path, os.path.pardir, os.path.pardir, "Pipfile")
    ),
}


def _delete_directory_if_exists(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)


def _cleanup():
    _delete_directory_if_exists(storage_path)
    _delete_directory_if_exists(local_repo_path)
    _delete_directory_if_exists(remote_repo_path)


def _prepare():
    os.makedirs(remote_repo_path)
    os.makedirs(local_repo_path)
    subprocess.check_call("git init", cwd=remote_repo_path, shell=True)
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


def test_cli_not_updated_if_no_pending_changes():
    _cleanup()
    _prepare()

    (
        as_a_user(local_repo_path)
        .run_hexagon(["echo"], os_env_vars, test_file_path_is_absolute=True)
        .then_output_should_be(["echo"])
        .exit()
    )

    _cleanup()


def test_cli_updated_if_pending_changes():
    _cleanup()
    _prepare()

    shutil.copyfile(
        os.path.join(test_folder_path, "modified-app.yml"),
        os.path.join(remote_repo_path, "app.yml"),
    )

    subprocess.check_call("git add .", cwd=remote_repo_path, shell=True)
    subprocess.check_call(
        "git -c user.name='Jhon Doe' -c user.email='my@email.org' commit -m modified",
        cwd=remote_repo_path,
        shell=True,
    )

    (
        as_a_user(local_repo_path)
        .run_hexagon(
            ["echo"],
            {
                **os_env_vars,
                "HEXAGON_THEME": "default",
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
            },
            test_file_path_is_absolute=True,
        )
        .write("y")
        .then_output_should_be(
            [
                "Updating",
                "Fast-forward",
                "app.yml | 2 +-",
                "1 file changed, 1 insertion(+), 1 deletion(-)",
                "would have ran pipenv install --system",
                "would have ran yarn --production",
                "Updated to latest version",
            ],
            True,
        )
        .exit()
    )

    _cleanup()


def test_dont_update_when_no_changes_on_current_branch():
    _cleanup()
    _prepare()

    shutil.copyfile(
        os.path.join(test_folder_path, "modified-app.yml"),
        os.path.join(remote_repo_path, "app.yml"),
    )
    subprocess.check_call("git add .", cwd=remote_repo_path, shell=True)
    subprocess.check_call(
        "git -c user.name='Jhon Doe' -c user.email='my@email.org' commit -m modified",
        cwd=remote_repo_path,
        shell=True,
    )

    subprocess.check_call("git checkout -b new-branch", cwd=local_repo_path, shell=True)

    (
        as_a_user(local_repo_path)
        .run_hexagon(
            ["echo"],
            {
                **os_env_vars,
                "HEXAGON_THEME": "default",
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
            },
            test_file_path_is_absolute=True,
        )
        .then_output_should_be(
            ["echo"],
            discard_until_first_match=True,
        )
        .exit(0)
    )

    _cleanup()


def test_update_when_changes_on_current_branch():
    _cleanup()
    _prepare()

    subprocess.check_call(
        "git checkout -b new-branch", cwd=remote_repo_path, shell=True
    )

    subprocess.check_call("git remote update", cwd=local_repo_path, shell=True)
    subprocess.check_call(
        "git checkout -b new-branch origin/new-branch", cwd=local_repo_path, shell=True
    )

    shutil.copyfile(
        os.path.join(test_folder_path, "modified-app.yml"),
        os.path.join(remote_repo_path, "app.yml"),
    )
    subprocess.check_call("git add .", cwd=remote_repo_path, shell=True)
    subprocess.check_call(
        "git -c user.name='Jhon Doe' -c user.email='my@email.org' commit -m modified",
        cwd=remote_repo_path,
        shell=True,
    )

    (
        as_a_user(local_repo_path)
        .run_hexagon(
            ["echo"],
            {
                **os_env_vars,
                "HEXAGON_THEME": "default",
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
            },
            test_file_path_is_absolute=True,
        )
        .write("y")
        .then_output_should_be(
            [
                "Updating",
                "Fast-forward",
                "app.yml | 2 +-",
                "1 file changed, 1 insertion(+), 1 deletion(-)",
                "would have ran pipenv install --system",
                "would have ran yarn --production",
                "Updated to latest version",
            ],
            True,
        )
        .exit(0)
    )

    _cleanup()


def test_cli_updates_fail_silently_if_not_in_a_git_repository():
    _cleanup()
    tmp_dir = tempfile.gettempdir()
    os.mkdir(local_repo_path)

    shutil.copyfile(
        os.path.join(test_folder_path, "app.yml"),
        os.path.join(tmp_dir, "app.yml"),
    )

    (
        as_a_user(tmp_dir)
        .run_hexagon(["echo"], os_env_vars, test_file_path_is_absolute=True)
        .then_output_should_be(["echo"])
        .exit()
    )

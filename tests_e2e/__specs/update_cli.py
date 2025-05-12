import os
import shutil
import subprocess

from tests_e2e.__specs.utils.hexagon_spec import as_a_user


def os_env_vars(test_folder_path):
    return {
        "HEXAGON_CLI_UPDATE_DISABLED": "false",
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


def test_cli_not_updated_if_no_pending_changes():
    spec = as_a_user(__file__)

    _prepare(spec.test_dir)

    (
        spec.run_hexagon(
            ["echo"],
            os_env_vars(spec.test_dir),
            test_dir=os.path.join(spec.test_dir, "local"),
        )
        .then_output_should_be(["echo"])
        .exit()
    )


def test_cli_updated_if_pending_changes():
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
            ["echo"],
            {
                **os_env_vars(spec.test_dir),
                "HEXAGON_THEME": "default",
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
            },
            test_dir=os.path.join(spec.test_dir, "local"),
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


def test_dont_update_when_no_changes_on_current_branch():
    spec = as_a_user(__file__)

    _prepare(spec.test_dir)

    remote_repo_path = os.path.join(spec.test_dir, "remote")
    local_repo_path = os.path.join(spec.test_dir, "local")

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

    subprocess.check_call("git checkout -b new-branch", cwd=local_repo_path, shell=True)

    (
        spec.run_hexagon(
            ["echo"],
            {
                **os_env_vars(spec.test_dir),
                "HEXAGON_THEME": "default",
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
            },
            test_dir=os.path.join(spec.test_dir, "local"),
        )
        .then_output_should_be(
            ["echo"],
            discard_until_first_match=True,
        )
        .exit(0)
    )


def test_update_when_changes_on_current_branch():
    spec = as_a_user(__file__)

    _prepare(spec.test_dir)

    remote_repo_path = os.path.join(spec.test_dir, "remote")
    local_repo_path = os.path.join(spec.test_dir, "local")

    subprocess.check_call(
        "git checkout -b new-branch", cwd=remote_repo_path, shell=True
    )

    subprocess.check_call("git remote update", cwd=local_repo_path, shell=True)
    subprocess.check_call(
        "git checkout -b new-branch origin/new-branch", cwd=local_repo_path, shell=True
    )

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
            ["echo"],
            {
                **os_env_vars(spec.test_dir),
                "HEXAGON_THEME": "default",
                "HEXAGON_DISABLE_DEPENDENCY_SCAN": "0",
                "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
            },
            test_dir=os.path.join(spec.test_dir, "local"),
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


def test_cli_updates_fail_silently_if_not_in_a_git_repository():
    spec = as_a_user(__file__)
    local_repo_path = os.path.join(spec.test_dir, "local")
    os.makedirs(local_repo_path, exist_ok=True)

    shutil.copyfile(
        os.path.join(spec.test_dir, "app.yml"),
        os.path.join(local_repo_path, "app.yml"),
    )

    (
        spec.run_hexagon(
            ["echo"],
            os_env_vars(spec.test_dir),
            test_dir=local_repo_path,
        )
        .then_output_should_be(["echo"])
        .exit()
    )

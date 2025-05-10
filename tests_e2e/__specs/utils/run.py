import os
import platform
import subprocess
import tempfile
from pathlib import Path
from shutil import copytree
from typing import Dict, List, Optional

from tests_e2e.__specs.utils.console import print
from tests_e2e.__specs.utils.path import e2e_test_folder_path

hexagon_path = os.path.realpath(
    os.path.join(
        os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir
    )
)

HEXAGON_COMMAND: List[str] = ["python", "-m", "hexagon"]
HEXAGON_COMMAND_DARWIN: List[str] = ["python3", "-m", "hexagon"]


def init_hexagon_e2e_test(test_file, test_dir: Optional[str] = None):
    test_folder_path = e2e_test_folder_path(test_file)

    tmp_dir = test_dir or tempfile.mkdtemp(suffix="_hexagon")
    copytree(test_folder_path, tmp_dir, dirs_exist_ok=True)
    return tmp_dir


def run_hexagon_e2e_test(
    args: List[str] = tuple(),
    yaml_file_name: str = "app.yml",
    os_env_vars: Optional[Dict[str, str]] = None,
    test_dir: Optional[str] = None,
) -> (str, subprocess.Popen[str]):
    if os_env_vars is None:
        os_env_vars = {}

    _set_env_vars_defaults(test_dir, os_env_vars)
    _create_required_dirs(os_env_vars)

    app_config_path = os.path.join(test_dir, *yaml_file_name.split("/"))
    if os.path.isfile(app_config_path):
        os_env_vars["HEXAGON_CONFIG_FILE"] = app_config_path

    os_env_vars["PYTHONPATH"] = hexagon_path

    return test_dir, run_hexagon_subprocess(test_dir, args, os_env_vars)


def _create_required_dirs(os_env_vars):
    Path(os_env_vars["HEXAGON_STORAGE_PATH"]).mkdir(parents=True, exist_ok=True)


def _set_env_vars_defaults(test_dir, os_env_vars):
    if "HEXAGON_TEST_SHELL" not in os_env_vars:
        os_env_vars["HEXAGON_TEST_SHELL"] = "HEXAGON_TEST_SHELL"
    if "HEXAGON_STORAGE_PATH" not in os_env_vars:
        os_env_vars["HEXAGON_STORAGE_PATH"] = os.path.join(test_dir, ".config")
    if "HEXAGON_THEME" not in os_env_vars:
        os_env_vars["HEXAGON_THEME"] = "result_only"
    if "HEXAGON_HINTS_DISABLED" not in os_env_vars:
        os_env_vars["HEXAGON_HINTS_DISABLED"] = "1"
    if "HEXAGON_UPDATE_DISABLED" not in os_env_vars:
        os_env_vars["HEXAGON_UPDATE_DISABLED"] = "1"
    if "HEXAGON_CLI_UPDATE_DISABLED" not in os_env_vars:
        os_env_vars["HEXAGON_CLI_UPDATE_DISABLED"] = "1"
    if "HEXAGON_SEND_TELEMETRY" not in os_env_vars:
        os_env_vars["HEXAGON_SEND_TELEMETRY"] = "0"
    if "HEXAGON_LOCALES_DIR" not in os_env_vars:
        os_env_vars["HEXAGON_LOCALES_DIR"] = os.path.join(hexagon_path, "locales")
    if "HEXAGON_DISABLE_DEPENDENCY_SCAN" not in os_env_vars:
        os_env_vars["HEXAGON_DISABLE_DEPENDENCY_SCAN"] = "1"
    if "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED" not in os_env_vars:
        os_env_vars["HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED"] = "1"


def run_hexagon_subprocess(
    cwd: str,
    args: List[str] = tuple(),
    os_env_vars: Optional[Dict[str, str]] = None,
):
    environment = os.environ.copy()
    if os_env_vars:
        environment.update(os_env_vars)

    command = []

    if platform.system() == "Darwin":
        command += HEXAGON_COMMAND_DARWIN
    else:
        command += HEXAGON_COMMAND

    command += args
    print(
        f"\n[dim]executing command:[/dim]\n{' '.join([f'{k}={v}' for k, v in environment.items() if 'HEXAGON_' in k] + command)}\n",
    )

    environment["COLUMNS"] = "200"
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        encoding="utf-8",
        cwd=cwd,
        env=environment,
        universal_newlines=True,
    )


def write_to_process(process: subprocess.Popen, input: str):
    written = process.stdin.write(input)
    if written != len(input):
        raise Exception(f"Written {written} instead of {input}")
    process.stdin.flush()


def clean_hexagon_environment():
    for key in os.environ:
        if "HEXAGON_" in key:
            del os.environ[key]

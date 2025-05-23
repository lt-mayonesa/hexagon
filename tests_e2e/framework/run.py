import os
import platform
import subprocess
import tempfile
from pathlib import Path
from shutil import copytree
from typing import Dict, List, Optional

from tests_e2e.framework.console import print
from tests_e2e.framework.path import e2e_test_folder_path

hexagon_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
)

HEXAGON_COMMAND: List[str] = ["python", "-m", "hexagon"]
HEXAGON_COMMAND_DARWIN: List[str] = ["python3", "-m", "hexagon"]


def init_hexagon_e2e_test(test_file, test_dir: Optional[str] = None):
    test_folder_path = e2e_test_folder_path(test_file)

    tmp_dir = test_dir or tempfile.mkdtemp(suffix="_hexagon")
    copytree(test_folder_path, tmp_dir, dirs_exist_ok=True)
    print(f"Initializing e2e test: {test_file}")
    print(f"Copied test folder from {test_folder_path} to {tmp_dir}")
    return tmp_dir


def run_hexagon_e2e_test(
    args: List[str] = tuple(),
    yaml_file_name: str = "app.yml",
    os_env_vars: Optional[Dict[str, str]] = None,
    installation_cwd: Optional[str] = None,
    execution_cwd: Optional[str] = None,
) -> (str, subprocess.Popen[str]):
    """
    Run hexagon in a subprocess setting the required environment variables.

    :param args: a list of command line arguments to pass to hexagon
    :param yaml_file_name: the name of the yaml file to use for the hexagon configuration
    :param os_env_vars: a dictionary of environment variables to set for the subprocess
    :param installation_cwd: directory where the yaml_file_name is located
    :param execution_cwd: directory where the subprocess will be executed
    :return:
    """
    os_env_vars = os_env_vars.copy() if os_env_vars is not None else {}

    _set_env_vars_defaults(installation_cwd, os_env_vars)
    _create_required_dirs(os_env_vars)

    app_config_path = os.path.join(installation_cwd, *yaml_file_name.split("/"))
    if os.path.isfile(app_config_path):
        os_env_vars["HEXAGON_CONFIG_FILE"] = app_config_path

    os_env_vars["PYTHONPATH"] = hexagon_path

    return installation_cwd, run_hexagon_subprocess(
        execution_cwd or installation_cwd, args, os_env_vars
    )


def _create_required_dirs(os_env_vars):
    Path(os_env_vars["HEXAGON_STORAGE_PATH"]).mkdir(parents=True, exist_ok=True)


def _set_env_vars_defaults(test_dir, os_env_vars):
    defaults = {
        "HEXAGON_CLI_UPDATE_DISABLED": "1",
        "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED": "1",
        "HEXAGON_DISABLE_DEPENDENCY_SCAN": "1",
        "HEXAGON_HINTS_DISABLED": "1",
        "HEXAGON_LOCALES_DIR": os.path.join(hexagon_path, "locales"),
        "HEXAGON_STORAGE_PATH": os.path.join(test_dir, ".config"),
        "HEXAGON_SEND_TELEMETRY": "0",
        "HEXAGON_TEST_SHELL": "HEXAGON_TEST_SHELL",
        "HEXAGON_THEME": "result_only",
        "HEXAGON_UPDATE_DISABLED": "1",
    }

    for key, value in defaults.items():
        if key not in os_env_vars:
            os_env_vars[key] = value


def run_hexagon_subprocess(
    execution_cwd: str, args: List[str], os_env_vars: Dict[str, str]
):
    environment = os.environ.copy()
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
        cwd=execution_cwd,
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

import itertools
import signal
import os
import subprocess
from typing import Dict, List, Optional
from e2e.tests.utils.path import e2e_test_folder_path

hexagon_path = os.path.realpath(
    os.path.join(
        os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir
    )
)

HEXAGON_COMMAND: List[str] = ["python", "-m", "hexagon"]


def run_hexagon_e2e_test(
    test_file: str,
    args: List[str] = tuple(),
    os_env_vars: Optional[Dict[str, str]] = None,
    test_file_path_is_absoulte: bool = False,
    cwd: str = None,
):
    if os_env_vars is None:
        os_env_vars = {}

    test_folder_path = (
        test_file if test_file_path_is_absoulte else e2e_test_folder_path(test_file)
    )

    os_env_vars["HEXAGON_TEST_SHELL"] = (
        os_env_vars["HEXAGON_TEST_SHELL"]
        if "HEXAGON_TEST_SHELL" in os_env_vars
        else "HEXAGON_TEST_SHELL"
    )

    if "HEXAGON_THEME" not in os_env_vars:
        os_env_vars["HEXAGON_THEME"] = "result_only"

    if "HEXAGON_UPDATE_DISABLED" not in os_env_vars:
        os_env_vars["HEXAGON_UPDATE_DISABLED"] = "1"

    if "HEXAGON_CLI_UPDATE_DISABLED" not in os_env_vars:
        os_env_vars["HEXAGON_CLI_UPDATE_DISABLED"] = "1"

    if "HEXAGON_DISABLE_SPINNER" not in os_env_vars:
        os_env_vars["HEXAGON_DISABLE_SPINNER"] = "1"

    if "HEXAGON_SEND_TELEMETRY" not in os_env_vars:
        os_env_vars["HEXAGON_SEND_TELEMETRY"] = "0"

    if "HEXAGON_LOCALES_DIR" not in os_env_vars:
        os_env_vars["HEXAGON_LOCALES_DIR"] = os.path.join(hexagon_path, "locales")

    os.environ["HEXAGON_STORAGE_PATH"] = os_env_vars.get(
        "HEXAGON_STORAGE_PATH",
        os.getenv("HEXAGON_STORAGE_PATH", os.path.join(test_folder_path, ".config")),
    )

    app_config_path = os.path.join(test_folder_path, "app.yml")
    if os.path.isfile(app_config_path):
        os_env_vars["HEXAGON_CONFIG_FILE"] = app_config_path

    os_env_vars["PYTHONPATH"] = hexagon_path

    return run_hexagon(cwd or test_folder_path, args, os_env_vars)


def run_hexagon(
    cwd: str,
    args: List[str] = tuple(),
    os_env_vars: Optional[Dict[str, str]] = None,
):
    environment = os.environ.copy()
    if os_env_vars:
        environment.update(os_env_vars)

    command = [*HEXAGON_COMMAND, *args]
    print(
        f"\nrunning command:\n{' '.join([f'{k}={v}' for k,v in environment.items() if 'HEXAGON_' in k] + command)}"
    )

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


def discard_output(process: subprocess.Popen, length: int):
    def timeout_handler(signum, frame):
        raise Exception("Timeout reading from process")

    for _ in itertools.repeat(None, length):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(3)
        process.stdout.readline()
        signal.alarm(0)


def clean_hexagon_environment():
    for key in os.environ:
        if "HEXAGON_" in key:
            del os.environ[key]

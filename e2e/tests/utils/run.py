import itertools
import signal
import os
import subprocess
from typing import Dict, List, Optional
from e2e.tests.utils.path import e2e_test_folder_path

hexagon_path = os.path.join(os.path.pardir, os.path.pardir, "hexagon")

HEXAGON_COMMAND: List[str]

try:
    subprocess.check_call(["pipenv", "--version"])
    HEXAGON_COMMAND = ["pipenv", "run", "python", hexagon_path]
except Exception:
    HEXAGON_COMMAND = ["python", hexagon_path]


def run_hexagon_e2e_test(
    test_file: str, args: List[str] = tuple(), env: Optional[Dict[str, str]] = None
):
    if env is None:
        env = {}

    test_folder_path = e2e_test_folder_path(test_file)

    env["HEXAGON_TEST_SHELL"] = (
        env["HEXAGON_TEST_SHELL"]
        if "HEXAGON_TEST_SHELL" in env
        else "HEXAGON_TEST_SHELL"
    )

    app_config_path = os.path.join(test_folder_path, "app.yml")
    if os.path.isfile(app_config_path):
        env["HEXAGON_CONFIG_FILE"] = app_config_path

    return run_hexagon(test_folder_path, args, env)


def run_hexagon(
    cwd: str, args: List[str] = tuple(), env: Optional[Dict[str, str]] = None
):
    environment = None
    if env:
        environment = os.environ.copy()
        environment.update(env)

    return subprocess.Popen(
        [*HEXAGON_COMMAND, *args],
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

from e2e.tests.utils.path import e2e_test_folder_path
import subprocess
import os
import itertools
from typing import Dict, List, Optional

hexagon_path = os.path.join(os.path.pardir, os.path.os.pardir, 'hexagon')

HEXAGON_COMMAND: List[str]

try:
    subprocess.check_call(['pipenv', '--version'])
    HEXAGON_COMMAND = ['pipenv', 'run', 'python', hexagon_path]
except Exception:
    HEXAGON_COMMAND = ['python', hexagon_path]


def run_hexagon_e2e_test(test_file: str, args: Optional[List[str]] = [], env: Optional[Dict[str, str]] = None):
    return run_hexagon(e2e_test_folder_path(test_file), args, env)


def run_hexagon(cwd: str, args: Optional[List[str]] = [], env: Optional[Dict[str, str]] = None):
    environment = None
    if env:
        environment = os.environ.copy()
        environment.update(env)

    return subprocess.Popen(
        [*HEXAGON_COMMAND, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        encoding='utf-8',
        cwd=cwd,
        env=environment,
        universal_newlines=True,
        bufsize=1
    )


def write_to_process(process: subprocess.Popen, input: str):
    process.stdin.write(input)
    process.stdin.flush()


def discard_output(process: subprocess.Popen, length: int):
    for _ in itertools.repeat(None, length):
        process.stdout.readline()

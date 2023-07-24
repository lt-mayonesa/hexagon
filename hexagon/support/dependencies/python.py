import sys
import subprocess
from typing import Optional

from hexagon.utils.fs import declarations_found

PYTHON_PIPFILE_NAME = "Pipfile"
PYTHON_REQUIREMENTS_NAME = "requirements.txt"
PYTHON_DEPENDENCY_FILES = [PYTHON_PIPFILE_NAME, PYTHON_REQUIREMENTS_NAME]


def scan_and_install_python_dependencies(path: str, mocked=False):
    for directory, files in declarations_found(path, PYTHON_DEPENDENCY_FILES):
        command: Optional[str] = None
        if PYTHON_REQUIREMENTS_NAME in files:
            command = f"python3 -m pip install -r {PYTHON_REQUIREMENTS_NAME}"
        elif PYTHON_PIPFILE_NAME in files:
            command = "pipenv install --system"

        if mocked:
            print(f"would have ran {command}")
        else:
            subprocess.check_call(
                command,
                shell=True,
                cwd=directory,
                stdout=sys.stdout,
                stderr=subprocess.DEVNULL,
            )

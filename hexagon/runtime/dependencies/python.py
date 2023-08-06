import subprocess
import sys
from typing import Optional

from hexagon.runtime.dependencies.fs import declarations_found
from hexagon.support.output.printer import log

PYTHON_PIPFILE_NAME = "Pipfile"
PYTHON_REQUIREMENTS_NAME = "requirements.txt"
PYTHON_DEPENDENCY_FILES = [PYTHON_PIPFILE_NAME, PYTHON_REQUIREMENTS_NAME]


def scan_and_install_python_dependencies(path: str, mocked=False):
    for directory, files in declarations_found(path, PYTHON_DEPENDENCY_FILES):
        with log.status(
            _("msg.support.dependencies.installing_dependencies").format(
                runtime="python", path=directory
            )
        ):
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

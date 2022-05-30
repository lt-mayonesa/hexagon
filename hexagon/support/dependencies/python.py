import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from hexagon.utils.fs import crawl_directory

PYTHON_PIPFILE_NAME = "Pipfile"
PYTHON_REQUIREMENTS_NAME = "requirements.txt"
PYTHON_DEPENDENCY_FILES = [PYTHON_PIPFILE_NAME, PYTHON_REQUIREMENTS_NAME]


def scan_and_install_python_dependencies(path: str, mocked=False):
    declarations_found: Dict[str, List[str]] = {}

    def add_declaration(key: str, file: Path):
        if key not in declarations_found:
            declarations_found[key] = []
        declarations_found[key].append(file)

    def crawler(file: Path):
        if file.name in PYTHON_DEPENDENCY_FILES:
            add_declaration(file.parent, file.name)

    crawl_directory(path, crawler)

    for (dir, files) in declarations_found.items():
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
                cwd=dir,
                stdout=sys.stdout,
                stderr=subprocess.DEVNULL,
            )

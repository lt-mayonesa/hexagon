import sys
import subprocess
from typing import Dict, List, Optional
from pathlib import Path

from hexagon.utils.fs import crawl_directory

PACKAGE_JSON_FILE_NAME = "package.json"
PACKAGE_JSON_LOCK_FILE_NAME = "package-lock.json"
YARN_LOCK_FILE_NAME = "yarn.lock"
NODEJS_DECLARATION_FILES = [
    PACKAGE_JSON_FILE_NAME,
    PACKAGE_JSON_LOCK_FILE_NAME,
    YARN_LOCK_FILE_NAME,
]


def scan_and_install_node_dependencies(path: str, mocked=False):
    declarations: Dict[str, List[str]] = {}

    def add_declaration(key: str, file: str):
        if key not in declarations:
            declarations[key] = []
        declarations[key].append(file)

    def crawler(file: Path):
        if file.name in NODEJS_DECLARATION_FILES:
            add_declaration(file.parent, file.name)

    crawl_directory(path, crawler)

    for (dir, files) in declarations.items():
        command: Optional[str] = None
        if PACKAGE_JSON_FILE_NAME in files:
            if YARN_LOCK_FILE_NAME in files and PACKAGE_JSON_LOCK_FILE_NAME in files:
                command = "npm install --only=production"
            elif YARN_LOCK_FILE_NAME in files:
                command = "yarn --production"
            else:
                command = "npm install --only=production"

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

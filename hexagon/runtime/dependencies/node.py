import subprocess
import sys
from typing import Optional

from hexagon.runtime.dependencies.fs import declarations_found
from hexagon.support.output.printer import log

PACKAGE_JSON_FILE_NAME = "package.json"
PACKAGE_JSON_LOCK_FILE_NAME = "package-lock.json"
YARN_LOCK_FILE_NAME = "yarn.lock"
NODEJS_DECLARATION_FILES = [
    PACKAGE_JSON_FILE_NAME,
    PACKAGE_JSON_LOCK_FILE_NAME,
    YARN_LOCK_FILE_NAME,
]


def scan_and_install_node_dependencies(path: str, mocked=False):
    for directory, files in declarations_found(path, NODEJS_DECLARATION_FILES):
        with log.status(
            _("msg.support.dependencies.installing_dependencies").format(
                runtime="node", path=path
            )
        ):
            command: Optional[str] = None
            if PACKAGE_JSON_FILE_NAME in files:
                if (
                    YARN_LOCK_FILE_NAME in files
                    and PACKAGE_JSON_LOCK_FILE_NAME in files
                ):
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
                    cwd=directory,
                    stdout=sys.stdout,
                    stderr=subprocess.DEVNULL,
                )

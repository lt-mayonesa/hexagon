import os

from hexagon.runtime.dependencies.node import scan_and_install_node_dependencies
from hexagon.runtime.dependencies.python import scan_and_install_python_dependencies
from hexagon.runtime.singletons import options

HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE = (
    "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED"
)


def scan_and_install_dependencies(path: str = None):
    if path is None:
        return

    if options.disable_dependency_scan:
        return

    mocked = (
        HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE in os.environ
        and os.environ[HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE]
        == "1"
    )

    scan_and_install_python_dependencies(path, mocked)

    scan_and_install_node_dependencies(path, mocked)

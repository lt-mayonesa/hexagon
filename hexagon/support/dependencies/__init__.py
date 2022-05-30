import os
from hexagon.support.dependencies.node import scan_and_install_node_dependencies
from hexagon.support.dependencies.python import scan_and_install_python_dependencies

HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE = (
    "HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED"
)


def scan_and_install_dependencies(path: str):
    if (
        "HEXAGON_DISABLE_DEPENDENCY_SCAN" in os.environ
        and os.environ["HEXAGON_DISABLE_DEPENDENCY_SCAN"] == "1"
    ):
        return

    mocked = (
        HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE in os.environ
        and os.environ[HEXAGON_DEPENDENCY_UPDATER_MOCK_ENABLED_ENVIRONMENT_VARIABLE]
        == "1"
    )
    scan_and_install_python_dependencies(path, mocked)
    scan_and_install_node_dependencies(path, mocked)

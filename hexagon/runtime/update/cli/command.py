import subprocess
import sys

from hexagon.runtime.singletons import configuration


def output_from_command_in_cli_project_path(command: str) -> str:
    return subprocess.check_output(
        command,
        shell=True,
        cwd=configuration.project_path,
        text=True,
        stderr=subprocess.DEVNULL,
    )


def execute_command_in_cli_project_path(
    command: str, show_stdout: bool = False
) -> None:
    assert (
        subprocess.check_call(
            command,
            shell=True,
            cwd=configuration.project_path,
            stdout=sys.stdout if show_stdout else subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        == 0
    )

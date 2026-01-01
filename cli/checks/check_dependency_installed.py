import subprocess

from hexagon.support.output.printer import log


def _is_installed(dependency):
    path = subprocess.check_output(["whereis", dependency])
    return path.decode("utf-8").strip() != f"{dependency}:"


def check_installed(dependency: str):
    if _is_installed(dependency):
        return
    else:
        log.panel(
            f"It seems you don't have [b]{dependency}[/b] installed.\n"
            f"Please install it and try again.",
            title="Invalid setup",
            color="red",
        )
        exit(1)

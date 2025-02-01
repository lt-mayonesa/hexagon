import os
import re
from enum import Enum

from InquirerPy.base import Choice

from hexagon.support.input.args import ToolArgs, PositionalArg, Arg
from hexagon.support.output.printer import log
from hexagon.support.storage import load_user_data, HexagonStorageKeys

HEXAGON_REGEX = re.compile("(HEXAGON_CONFIG_FILE=)([/A-Za-z0-9\\-_.]+)\\s(hexagon)")


class Action(Enum):
    UNINSTALL = "uninstall"
    CONFIGURE = "configure"
    LIST_TOOLS = "list_tools"
    NOTHING = "nothing"


class Args(ToolArgs):
    cli: PositionalArg[str] = Arg(
        None, searchable=True, prompt_message="Installed CLIs"
    )
    action: PositionalArg[Action] = Arg(
        None,
        prompt_message="What do you want to do with the CLI?",
    )


def main(_, __, ___, cli_args: Args):
    bins_path = load_user_data(HexagonStorageKeys.cli_install_path.value)

    if not bins_path:
        log.panel(
            "No hexagon [b]bins[/b] path configured yet.\n"
            "Please run [b]hexagon install[/b] to install your first CLI and set it up.",
            justify="center",
        )
        exit(1)

    if not cli_args.cli.value:
        choices = [
            Choice(binary, name=f"{binary:<40}{target_yaml}")
            for binary, target_yaml in __find_hexagon_bins(bins_path)
        ]
        if not choices:
            log.panel(
                f"No hexagon [b]CLIs[/b] found in the configured bins path: [b]{bins_path}[/b].\n"
                "Please run [b]hexagon install[/b] to install your first CLI and set it up.",
                title="Unexpected error",
                color="red",
                justify="center",
            )
            exit(1)
        cli_args.cli.prompt(
            choices=choices,
        )

    full_path, target_yaml = __get_from_bin(cli_args.cli.value, bins_path)
    log.gap()
    log.file(target_yaml, line_range=(0, 12), code_width=80)
    log.info("-- and more --", gap_end=1)

    if not cli_args.action.value:
        cli_args.action.prompt(skip_trace=True)

    if cli_args.action.value == Action.UNINSTALL:
        log.info(f"Uninstalling {cli_args.cli.value}")

        log.result(f"[green]✓ {cli_args.cli.value} uninstalled")
    elif cli_args.action.value == Action.CONFIGURE:
        log.info(f"Configuring {cli_args.cli.value}")

        log.result(f"[green]✓ {cli_args.cli.value} configured")
    elif cli_args.action.value == Action.LIST_TOOLS:
        log.info(f"Listing tools for {cli_args.cli.value}")

        log.result(f"[green]✓ {cli_args.cli.value} tools listed")


def __find_hexagon_bins(directory):
    for root, _dirs, files in os.walk(directory, onerror=log.error):
        for filename in files:
            try:
                with open(os.path.join(root, filename), "r") as file:
                    for line in file.readlines():
                        match = HEXAGON_REGEX.search(line)
                        if match:
                            yield filename, match.group(2)
            except ValueError:
                pass


def __get_from_bin(binary, bins_path):
    binary_path = os.path.join(bins_path, binary)
    with open(binary_path, "r") as file:
        for line in file.readlines():
            match = HEXAGON_REGEX.search(line)
            if match:
                return binary_path, match.group(2)

from hexagon.runtime.execute.tool import select_and_execute_tool
from hexagon.runtime.parse_args import parse_cli_args
from hexagon.runtime.singletons import tools, envs
from hexagon.support.output.printer import log
from hexagon.support.storage import (
    HexagonStorageKeys,
    load_user_data,
)


def main(tool, env, env_args, cli_args):
    last_command = load_user_data(HexagonStorageKeys.last_command.value)

    log.info(
        _("msg.actions.internal.replay.last_command").format(last_command=last_command)
    )

    args = parse_cli_args(last_command.split(" ")[1:])

    return select_and_execute_tool(tools, envs, args)

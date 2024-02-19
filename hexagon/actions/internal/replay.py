import re

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

    to_list = __command_str_to_list(last_command)
    args = parse_cli_args(to_list[1:])

    return select_and_execute_tool(tools, envs, args)


def __command_str_to_list(last_command: str):
    """
    last_command will be something like:
    hexagon-test python-module john 10 --country="The Netherlands" --likes=orange
    or
    hexagon-test python-module john 10 --country='The Netherlands' --likes=orange
    simulate sys.argv behavior and return something like:
    ['hexagon-test', 'python-module', 'john', '10', '--country=The Netherlands', '--likes=orange']
    """
    split = re.findall(r'(?:"[^"]*"|\'[^\']*\'|[^\s"\'])+', last_command)
    split = [__remove_wrapping_quotes(item) for item in split]
    return split


def __remove_wrapping_quotes(item):
    match = re.match(r'(-+\w+=)*(?:(")[^"]*("))+', item, re.IGNORECASE)
    if match:
        return re.sub(r'"', "", item)
    match = re.match(r"(-+\w+=)*(?:(')[^']*('))+", item, re.IGNORECASE)
    if match:
        return re.sub(r"'", "", item)
    return item

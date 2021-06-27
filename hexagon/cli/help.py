from itertools import groupby

from rich import print


def print_help(cli_config: dict, tools: dict, envs: dict):
    """
    Print the command line help text based on the tools and envs in configuration yaml

    :param cli_config:
    :param tools:
    :param envs:
    :return:
    """
    if cli_config["name"] == "Hexagon":
        print("│ [bold]Hexagon")
        print("│")
        print("│ You are executing Hexagon without an install.")
        print('│ To get started run hexagon\'s "Install Hexagon" tool')
        return

    print(f'│ [bold]{cli_config["name"]}')

    print("│")
    print("│ [bold][u]Envs:")
    for k, v in envs.items():
        print(f'│   {k + (" (" + v["alias"] + ")" if "alias" in v else "")}')

    print("│")
    print("│")
    print("│ [bold][u]Tools:")

    def key_func(z):
        x, y = z
        return y["type"]

    data = sorted(tools.items(), key=key_func, reverse=True)

    for gk, g in groupby(data, key_func):
        print("│")
        print(f"│ [bold]{gk}:")

        for k, v in g:
            print(
                f'│   {k + (" (" + v["alias"] + ")" if "alias" in v else ""):<60}[dim]{v.get("long_name", "")}'
            )
            if "description" in v:
                print(f'│   {"": <60}[dim]{v["description"]}')
                print("│")

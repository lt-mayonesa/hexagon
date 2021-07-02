import webbrowser

from hexagon.cli.printer import log


def main(tool, env, env_args, cli_args):
    url = env_args
    log.result("Abriendo link: " + url)
    webbrowser.open(url)

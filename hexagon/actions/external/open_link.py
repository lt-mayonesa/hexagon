import webbrowser

from hexagon.support.printer import log


def main(tool, env, env_args, cli_args):
    url = env_args
    log.result("Opening url: " + url)
    webbrowser.open(url)

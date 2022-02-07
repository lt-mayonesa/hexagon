import webbrowser

from hexagon.support.printer import log


def main(tool, env, env_args, cli_args):
    url = env_args
    log.result(_("msg.actions.external.open_link.result").format(url=url))
    webbrowser.open(url)

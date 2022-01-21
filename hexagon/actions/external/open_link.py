import webbrowser

from hexagon.support.printer import log, translator

_ = translator


def main(tool, env, env_args, cli_args):
    url = env_args
    log.result(_("msg.actions.external.open_link.result").format(url=url))
    webbrowser.open(url)

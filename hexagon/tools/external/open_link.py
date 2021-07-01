import webbrowser

from hexagon.cli.printer import log


def main(url):
    log.result("Abriendo link: " + url)
    webbrowser.open(url)

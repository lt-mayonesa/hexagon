from typing import Callable

from rich.console import Console

from hexagon.support.printer.logger import Logger
from hexagon.support.printer.themes import load_theme
from hexagon.support.printer.i18n import install

theme = load_theme()

log = Logger(Console(color_system="auto" if theme.show_colors else None), theme)

translator: Callable[[str], str] = install()

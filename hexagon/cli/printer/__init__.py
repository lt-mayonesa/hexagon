from rich.console import Console

from hexagon.cli.printer.logger import Logger
from hexagon.cli.printer.themes import load_theme

theme = load_theme()

log = Logger(
    Console(color_system="auto" if theme.show_colors else None),
    theme,
)

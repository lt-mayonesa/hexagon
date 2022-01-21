import os
from typing import Callable

from rich.console import Console

from hexagon.support.printer.logger import Logger
from hexagon.support.printer.themes import load_theme

import gettext

LOCALEDIR = os.environ.get("HEXAGON_LOCALES_DIR", "locales")

theme = load_theme()

log = Logger(Console(color_system="auto" if theme.show_colors else None), theme)

try:
    el = gettext.translation("hexagon", localedir=LOCALEDIR)
except FileNotFoundError:
    el = gettext.translation(
        "hexagon", localedir=LOCALEDIR, languages=["en"], fallback=True
    )
el.install()

translator: Callable[[str], str] = el.gettext

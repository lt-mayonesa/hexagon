import os

from .configuration import Configuration
from .options import get_options
from hexagon.support.printer import log

CONFIG_FILE_ENV_VARIABLE_NAME = "HEXAGON_CONFIG_FILE"

log.load_theme(os.getenv("HEXAGON_THEME", "default"))

configuration = Configuration()
cli, tools, envs = configuration.init_config(
    os.getenv(CONFIG_FILE_ENV_VARIABLE_NAME, "app.yaml")
)
options = get_options(cli.options or {})

log.load_theme(options.theme)

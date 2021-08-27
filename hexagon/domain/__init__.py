import os

from .configuration import Configuration
from .options import get_options

CONFIG_FILE_ENV_VARIABLE_NAME = "HEXAGON_CONFIG_FILE"

options = get_options()
configuration = Configuration()
cli, tools, envs = configuration.init_config(
    os.getenv(CONFIG_FILE_ENV_VARIABLE_NAME, "app.yaml")
)

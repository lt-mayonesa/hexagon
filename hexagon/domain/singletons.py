import os

from . import CONFIG_FILE_ENV_VARIABLE_NAME
from .configuration import Configuration
from .options import get_options

configuration = Configuration()
cli, tools, envs = configuration.init_config(
    os.getenv(CONFIG_FILE_ENV_VARIABLE_NAME, "app.yaml")
)
options = get_options(cli.options or {})

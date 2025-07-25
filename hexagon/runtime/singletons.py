import os

from hexagon.domain import CONFIG_FILE_ENV_VARIABLE_NAME
from hexagon.runtime.configuration import Configuration
from hexagon.runtime.cwd_tools import collect_cwd_tools
from hexagon.runtime.options import get_options

configuration = Configuration()
cli, tools, envs = configuration.init_config(
    os.getenv(CONFIG_FILE_ENV_VARIABLE_NAME, "app.yaml")
)
options = get_options(cli.options or {})

_cwd_tools = collect_cwd_tools(options)
if _cwd_tools:
    cli, tools, envs = configuration.add_tools(_cwd_tools.tools)

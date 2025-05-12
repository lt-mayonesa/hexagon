import os

from hexagon.domain import HEXAGON_CWD_TOOLS_FILE_NAME
from hexagon.domain.tool import OnlyToolsFile
from hexagon.runtime.options import Options
from hexagon.runtime.yaml import read_file, load_model


def collect_cwd_tools(options: Options):
    """
    Collects all tools from the current working directory and registers them in the configuration.
    :param options:
    """
    if options.cwd_tools_disabled:
        return None

    extra_tools_file = os.path.join(os.getcwd(), HEXAGON_CWD_TOOLS_FILE_NAME + ".yaml")
    if not os.path.exists(extra_tools_file):
        extra_tools_file = os.path.join(
            os.getcwd(), HEXAGON_CWD_TOOLS_FILE_NAME + ".yml"
        )

    if not os.path.exists(extra_tools_file):
        return None

    extra_tools_yaml = read_file(extra_tools_file)

    if not extra_tools_yaml:
        return None

    return load_model(OnlyToolsFile, extra_tools_yaml, extra_tools_file)

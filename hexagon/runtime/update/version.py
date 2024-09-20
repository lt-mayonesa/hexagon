import json
import sys
from urllib.request import Request, urlopen

from packaging.version import parse as parse_version

from hexagon.runtime.update import REPO_NAME


def local(override=None):
    return parse_version(override or _local_version())


def _local_version():
    if sys.version_info >= (3, 8):
        import importlib.metadata as importlib_metadata

        return importlib_metadata.version("hexagon")
    else:
        import pkg_resources

        return pkg_resources.require("hexagon")[0].version


def latest(override: str = None):
    latest_release_request = Request(
        override or f"https://pypi.org/pypi/{REPO_NAME}/json"
    )
    latest_pypi_release = json.load(urlopen(latest_release_request))
    return parse_version(latest_pypi_release["info"]["version"])

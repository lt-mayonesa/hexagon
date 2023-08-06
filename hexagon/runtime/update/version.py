import json
import sys
from urllib.request import Request, urlopen

from packaging.version import parse as parse_version

from hexagon.runtime.update import REPO_NAME, REPO_ORG
from hexagon.runtime.update.github import add_github_access_token


def local(override=None):
    return parse_version(override or _local_version())


def _local_version():
    if sys.version_info >= (3, 8):
        import importlib.metadata as importlib_metadata

        return importlib_metadata.version("hexagon")
    else:
        import pkg_resources

        return pkg_resources.require("hexagon")[0].version


def latest():
    latest_release_request = Request(
        f"https://api.github.com/repos/{REPO_ORG}/{REPO_NAME}/releases/latest"
    )
    add_github_access_token(latest_release_request)
    latest_github_release = json.load(urlopen(latest_release_request))
    return parse_version(latest_github_release["name"].replace("v", ""))

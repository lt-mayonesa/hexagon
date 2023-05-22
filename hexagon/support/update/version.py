import importlib.metadata as importlib_metadata
import json
import os
import sys
from urllib.request import Request, urlopen

import pkg_resources
from packaging.version import parse as parse_version

from hexagon.support.github import add_github_access_token
from hexagon.support.update import REPO_NAME, REPO_ORG


def local():
    return parse_version(
        os.getenv("HEXAGON_TEST_VERSION_OVERRIDE")
        if "HEXAGON_TEST_VERSION_OVERRIDE" in os.environ
        else _local_version()
    )


def _local_version():
    if sys.version_info >= (3, 8):
        return importlib_metadata.version("hexagon")
    else:
        return pkg_resources.require("hexagon")[0].version


def latest():
    latest_release_request = Request(
        f"https://api.github.com/repos/{REPO_ORG}/{REPO_NAME}/releases/latest"
    )
    add_github_access_token(latest_release_request)
    latest_github_release = json.load(urlopen(latest_release_request))
    return parse_version(latest_github_release["name"].replace("v", ""))

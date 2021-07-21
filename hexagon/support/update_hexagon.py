import pkg_resources
import json
import os
import subprocess
import sys
from urllib.request import urlopen
from packaging.version import parse as parse_version
from hexagon.support.printer import log
from hexagon.support.storage import (
    store_user_data,
    load_user_data,
    HEXAGON_STORAGE_APP,
    HexagonStorageKeys,
)
from InquirerPy import inquirer
import datetime

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"
REPO_ORG = "redbeestudios"
REPO_NAME = "hexagon"


def __already_checked():
    last_checked = load_user_data(
        HexagonStorageKeys.last_update_check.value, HEXAGON_STORAGE_APP
    )

    result = False

    if last_checked:
        last_checked_date = datetime.datetime.strptime(
            last_checked, LAST_UPDATE_DATE_FORMAT
        ).date()

        # TODO: Move to hexagon configuration
        # See https://github.com/redbeestudios/hexagon/pull/35#discussion_r670870804 for more information
        result = last_checked_date >= datetime.date.today()

    if not result:
        store_user_data(
            HexagonStorageKeys.last_update_check.value,
            datetime.date.today().strftime(LAST_UPDATE_DATE_FORMAT),
            app=HEXAGON_STORAGE_APP,
        )

    return result


def check_for_hexagon_updates():
    if bool(os.getenv("HEXAGON_UPDATE_DISABLED")):
        return
    if __already_checked():
        return

    current_version = os.getenv(
        "HEXAGON_TEST_VERSION_OVERRIDE", pkg_resources.require("hexagon")[0].version
    )

    latest_github_release = json.load(
        urlopen(f"https://api.github.com/repos/{REPO_ORG}/{REPO_NAME}/releases/latest")
    )
    latest_github_release_version = latest_github_release["name"].replace("v", "")

    if parse_version(current_version) >= parse_version(latest_github_release_version):
        return

    log.info(
        f"New [cyan]hexagon [white]version available [green]{latest_github_release_version}[white]!"
    )

    if not inquirer.confirm("Would you like to update?", default=True).execute():
        return

    subprocess.check_call(
        f"{sys.executable} -m pip install https://github.com/{REPO_ORG}/{REPO_NAME}/releases/download/v{latest_github_release_version}/hexagon-{latest_github_release_version}.tar.gz",
        shell=True,
        stdout=subprocess.DEVNULL,
    )
    log.info("[green]✔️ [white]Updated to latest version")
    log.finish()
    sys.exit(1)

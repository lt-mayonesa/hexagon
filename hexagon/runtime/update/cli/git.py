import re
from typing import Optional

from hexagon.runtime.update.cli.command import output_from_command_in_cli_project_path
from hexagon.support.storage import load_user_data, store_user_data


class CliGitConfig:
    def __init__(self, remote: str, head_branch: str) -> None:
        self.remote = remote
        self.head_branch = head_branch

    remote: str
    head_branch: str


CLI_GIT_CONFIG_STORAGE_KEY = "git-config"


def load_cli_git_config() -> Optional[CliGitConfig]:
    raw_data = load_user_data(CLI_GIT_CONFIG_STORAGE_KEY)
    try:
        write_dict = {}
        remote = raw_data["remote"] if raw_data and "remote" in raw_data else None
        if not remote:
            remotes = output_from_command_in_cli_project_path("git remote").splitlines()
            if len(remotes) == 1:
                remote = remotes[0]
            elif "origin" in remotes:
                remote = "origin"
            else:
                raise Exception(_("error.support.cli.git.failed_to_get_remote"))

            write_dict["remote"] = remote

        head_branch = (
            raw_data["head_branch"] if raw_data and "head_branch" in raw_data else None
        )
        if not head_branch:
            output = output_from_command_in_cli_project_path(
                f"git remote show {remote}"
            )
            head_branch = re.search(r"HEAD branch: (.+)", output).groups(0)[0]
            write_dict["head_branch"] = head_branch

        if write_dict:
            store_user_data(CLI_GIT_CONFIG_STORAGE_KEY, write_dict, append=True)

        return CliGitConfig(remote, head_branch)
    except Exception:
        return None

import os
from urllib.request import Request, urlopen

from hexagon.runtime.update.github import add_github_access_token


class ChangelogFile(object):
    def __init__(self, file):
        self.file = file

    def line(self):
        raise NotImplementedError("Please Implement this method")


class LocalChangelogFile(ChangelogFile):
    def line(self):
        return self.file.readline()


class RemoteChangelogFile(ChangelogFile):
    def line(self):
        return self.file.readline().decode(self.file.headers.get_content_charset())


def fetch_changelog(repo_org: str, repo_name: str):
    request = Request(
        f"https://api.github.com/repos/{repo_org}/{repo_name}/contents/CHANGELOG.md"
    )
    request.add_header("Accept", "application/vnd.github.3.raw")
    add_github_access_token(request)
    changelog_file_path = os.getenv("HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE")
    return (
        LocalChangelogFile(open(changelog_file_path, "r"))
        if changelog_file_path
        else RemoteChangelogFile(urlopen(request))
    )

import os
from urllib.request import Request, urlopen

from hexagon.runtime.update.github import add_github_access_token


class ChangelogFile(object):
    def __init__(self, file):
        self.file = file

    def readlines(self):
        raise NotImplementedError("Please Implement this method")


class LocalChangelogFile(ChangelogFile):
    def readlines(self):
        return self.file.readlines()


class RemoteChangelogFile(ChangelogFile):
    def readlines(self):
        charset = self.file.headers.get_content_charset() or "utf-8"
        return [line.decode(charset) for line in self.file.readlines()]


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

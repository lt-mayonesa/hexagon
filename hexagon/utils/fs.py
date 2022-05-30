from typing import Callable, List, Optional

import os
import subprocess
from pathlib import Path


def crawl_directory(
    path: str,
    run: Callable[[Path], None],
    ignored_dirs: Optional[List[str]] = None,
    ignore_dirs_ignored_by_git=True,
    in_git_repo: Optional[bool] = None,
):
    if ignored_dirs is None:
        ignored_dirs = []

    if ignore_dirs_ignored_by_git and in_git_repo is None:
        in_git_repo = (
            subprocess.call(
                "git rev-parse --is-inside-work-tree",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            == 0
        )

    use_gitignore = ignore_dirs_ignored_by_git and in_git_repo

    if (
        use_gitignore
        and subprocess.call(
            "git check-ignore {root}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        == 0
    ):
        return

    for root, dirs, files in os.walk(path):
        for file in files:
            run(Path(os.path.join(root, file)))
        for dir in dirs:
            if dir in ignored_dirs or dir in [".git"]:
                continue
            crawl_directory(
                os.path.join(root, dir),
                run,
                ignored_dirs=ignored_dirs,
                ignore_dirs_ignored_by_git=ignore_dirs_ignored_by_git,
                in_git_repo=in_git_repo,
            )

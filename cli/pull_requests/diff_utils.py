"""
Utilities for parsing and filtering unified diffs.

This module provides functions for working with git-style unified diffs,
including parsing diffs into per-file chunks and filtering files that
should be skipped (lock files, large generated files, etc.).
"""

from typing import Dict, List, Tuple

# Lock file patterns to skip when displaying diffs
LOCK_FILE_PATTERNS = [
    "poetry.lock",
    "package-lock.json",
    "yarn.lock",
    "Cargo.lock",
    "Gemfile.lock",
    "composer.lock",
    "pnpm-lock.yaml",
]

# Maximum number of changed lines before skipping a file as "too large"
MAX_FILE_CHANGES_THRESHOLD = 200


def parse_diff_by_file(diff_text: str) -> Dict[str, str]:
    """
    Parse a unified diff into separate chunks per file.

    Takes a git unified diff and splits it into individual diffs for each file,
    keyed by the file path.

    Args:
        diff_text: Full unified diff text from git

    Returns:
        Dictionary mapping file paths to their diff content

    Example:
        >>> diff = '''diff --git a/file1.txt b/file1.txt
        ... --- a/file1.txt
        ... +++ b/file1.txt
        ... @@ -1 +1 @@
        ... -old
        ... +new'''
        >>> diffs = parse_diff_by_file(diff)
        >>> 'file1.txt' in diffs
        True
    """
    file_diffs = {}
    current_file = None
    current_diff_lines = []

    for line in diff_text.split("\n"):
        # Check if this is a new file diff header
        if line.startswith("diff --git"):
            # Save previous file if exists
            if current_file:
                file_diffs[current_file] = "\n".join(current_diff_lines)

            # Extract filename from "diff --git a/path/to/file b/path/to/file"
            parts = line.split()
            if len(parts) >= 3:
                current_file = parts[2][2:]  # Remove "a/" prefix
                current_diff_lines = [line]
        elif current_file:
            current_diff_lines.append(line)

    # Don't forget the last file
    if current_file:
        file_diffs[current_file] = "\n".join(current_diff_lines)

    return file_diffs


def should_skip_file(
    file_path: str, additions: int, deletions: int
) -> Tuple[bool, str]:
    """
    Determine if a file should be skipped when displaying diffs.

    Files are skipped if they are:
    1. Lock files (poetry.lock, package-lock.json, etc.)
    2. Very large files (> MAX_FILE_CHANGES_THRESHOLD lines changed)

    Args:
        file_path: Path to the file
        additions: Number of lines added
        deletions: Number of lines deleted

    Returns:
        Tuple of (should_skip: bool, reason: str)
        If should_skip is True, reason contains a human-readable explanation

    Example:
        >>> should_skip_file("poetry.lock", 1000, 500)
        (True, 'large lock file')
        >>> should_skip_file("README.md", 5, 2)
        (False, '')
    """
    # Check if it's a lock file
    for pattern in LOCK_FILE_PATTERNS:
        if pattern in file_path:
            return True, "large lock file"

    # Check if file has too many changes
    total_changes = additions + deletions
    if total_changes > MAX_FILE_CHANGES_THRESHOLD:
        return True, f"large file ({total_changes} lines changed)"

    return False, ""


def get_files_to_display(files: List[dict]) -> Tuple[List[dict], List[dict]]:
    """
    Filter a list of files into those to display and those to skip.

    Args:
        files: List of file dictionaries with 'path', 'additions', 'deletions' keys

    Returns:
        Tuple of (files_to_display, skipped_files)
        Each is a list of dicts with file info and skip reason (for skipped files)

    Example:
        >>> files = [
        ...     {'path': 'README.md', 'additions': 5, 'deletions': 2},
        ...     {'path': 'poetry.lock', 'additions': 1000, 'deletions': 500}
        ... ]
        >>> to_display, skipped = get_files_to_display(files)
        >>> len(to_display)
        1
        >>> len(skipped)
        1
    """
    files_to_display = []
    skipped_files = []

    for file_info in files:
        file_path = file_info.get("path", "")
        additions = file_info.get("additions", 0)
        deletions = file_info.get("deletions", 0)

        should_skip, reason = should_skip_file(file_path, additions, deletions)

        if should_skip:
            skipped_files.append(
                {
                    **file_info,
                    "skip_reason": reason,
                }
            )
        else:
            files_to_display.append(file_info)

    return files_to_display, skipped_files

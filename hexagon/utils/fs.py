from pathlib import Path
from typing import List, Dict


def declarations_found(path: str, dependency_files: List[str]):
    matches: Dict[Path, List[str]] = {}

    for f in dependency_files:
        for p in Path(path).rglob(f):
            if p.parent not in matches:
                matches[p.parent] = []
            matches[p.parent].append(p.name)

    return list(matches.items())

from functools import reduce
from typing import List

from hexagon.runtime.update.changelog import ChangelogVersionEntry, ChangelogEntry

CHANGELOG_TYPE_FEATURE = "Feature"
CHANGELOG_TYPE_FIX = "Fix"
CHANGELOG_TYPE_DOCUMENTATION = "Documentation"

CHANGELOG_ENTRY_TYPE_ORDER_MAP = {
    CHANGELOG_TYPE_FEATURE: 2,
    CHANGELOG_TYPE_FIX: 1,
    CHANGELOG_TYPE_DOCUMENTATION: 0,
}


def __reducer(acc: List[ChangelogEntry], version: ChangelogVersionEntry):
    acc.extend(version.entries)
    return acc


def format_entries(entries: List[ChangelogVersionEntry]):
    entries = [
        entry
        for entry in reduce(
            __reducer,
            entries,
            [],
        )
        if entry.type in CHANGELOG_ENTRY_TYPE_ORDER_MAP.keys()
    ]
    entries.sort(key=lambda e: CHANGELOG_ENTRY_TYPE_ORDER_MAP[e.type], reverse=True)
    return entries

from typing import List


class ChangelogEntry:
    type: str
    message: str

    def __init__(self, type: str, message: str):
        self.type = type
        self.message = message

    def __str__(self):
        return "{type}: {message}".format(type=self.type, message=self.message)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.type, self.message) == (other.type, other.message)


class ChangelogVersionEntry:
    version: str
    entries: List[ChangelogEntry]

    def __init__(self, version: str):
        self.version = version
        self.entries = []

    def __str__(self):
        return "{version}\n{entries}".format(
            version=self.version, entries="\n".join([f"\t{e}" for e in self.entries])
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.version, self.entries) == (other.version, other.entries)

from pathlib import Path
from typing import Any

from pydantic import (
    FilePath as PydanticFilePath,
    DirectoryPath as PydanticDirectoryPath,
    errors,
)

FilePath = PydanticFilePath

DirectoryPath = PydanticDirectoryPath


def path_validator(v: Any) -> Path:
    if isinstance(v, Path):
        return v

    try:
        return Path(v)
    except TypeError:
        raise errors.PathError()

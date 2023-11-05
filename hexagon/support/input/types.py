from copy import copy
from pathlib import Path
from typing import Any

from pydantic import (
    FilePath as PydanticFilePath,
    DirectoryPath as PydanticDirectoryPath,
    errors,
)
from pydantic.errors import _PathValueError


class FileNotExistsError(_PathValueError):
    code = "path.not_exists"
    msg_template = 'file at path "{path}" does not exist.'


class DirectoryNotExistsError(_PathValueError):
    code = "path.not_exists"
    msg_template = 'directory at path "{path}" does not exist.'


class FilePath(PydanticFilePath):
    @classmethod
    def __get_validators__(cls, *args, **kwargs):
        yield path_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: Path, field) -> Path:
        declaration_extras = copy(field.field_info.extra)

        if declaration_extras.get("allow_nonexistent", True):
            if not value.exists():
                raise FileNotExistsError(path=value)

            if not value.is_file():
                raise errors.PathNotAFileError(path=value)

        return value


class DirectoryPath(PydanticDirectoryPath):
    @classmethod
    def __get_validators__(cls):
        yield path_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: Path, field) -> Path:
        declaration_extras = copy(field.field_info.extra)

        if declaration_extras.get("allow_nonexistent", True):
            if not value.exists():
                raise DirectoryNotExistsError(path=value)

            if not value.is_dir():
                raise errors.PathNotADirectoryError(path=value)

        return value


def path_validator(v: Any) -> Path:
    if isinstance(v, Path):
        return v

    try:
        return Path(v)
    except TypeError:
        raise errors.PathError()
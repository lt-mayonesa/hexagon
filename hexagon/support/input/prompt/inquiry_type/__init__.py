from enum import Enum, auto
from pathlib import Path


class InquiryType(Enum):
    STRING = auto()
    STRING_SEARCHABLE = auto()
    STRING_LIST = auto()
    STRING_LIST_SEARCHABLE = auto()
    ENUM = auto()
    ENUM_SEARCHABLE = auto()
    ENUM_LIST = auto()
    ENUM_LIST_SEARCHABLE = auto()
    PATH = auto()
    PATH_SEARCHABLE = auto()
    INT = auto()
    FLOAT = auto()
    SECRET = auto()
    BOOLEAN = auto()


def determine_expected_inquiry(iterable, of_enum, field_type, extras) -> InquiryType:
    searchable = extras.get("searchable", False)

    query = InquiryType.STRING if not searchable else InquiryType.STRING_SEARCHABLE
    if iterable and of_enum:
        query = (
            InquiryType.ENUM_LIST
            if not searchable
            else InquiryType.ENUM_LIST_SEARCHABLE
        )
    elif iterable:
        query = (
            InquiryType.STRING_LIST
            if not searchable
            else InquiryType.STRING_LIST_SEARCHABLE
        )
    elif of_enum:
        query = InquiryType.ENUM if not searchable else InquiryType.ENUM_SEARCHABLE
    elif issubclass(field_type.base_type, Path):
        query = InquiryType.PATH if not searchable else InquiryType.PATH_SEARCHABLE
    elif issubclass(field_type.base_type, bool):
        query = InquiryType.BOOLEAN
    elif issubclass(field_type.base_type, int):
        query = InquiryType.INT
    elif issubclass(field_type.base_type, float):
        query = InquiryType.FLOAT
    elif extras.get("secret", False):
        query = InquiryType.SECRET

    return query

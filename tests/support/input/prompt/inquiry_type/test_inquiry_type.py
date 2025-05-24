from enum import Enum, auto
from pathlib import Path
from typing import List

from hexagon.support.input.prompt.inquiry_type import (
    InquiryType,
    determine_expected_inquiry,
)


class TestEnum(Enum):
    OPTION_A = auto()
    OPTION_B = auto()


class MockTypeInformation:
    def __init__(self, base_type):
        self.base_type = base_type
        self.is_directory_path = False


def test_determine_expected_inquiry_returns_string_type():
    field_type = MockTypeInformation(str)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.STRING


def test_determine_expected_inquiry_returns_string_searchable_type():
    field_type = MockTypeInformation(str)
    inquiry_type = determine_expected_inquiry(
        False, False, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.STRING_SEARCHABLE


def test_determine_expected_inquiry_returns_string_list_type():
    field_type = MockTypeInformation(List[str])
    inquiry_type = determine_expected_inquiry(True, False, field_type, {})
    assert inquiry_type == InquiryType.STRING_LIST


def test_determine_expected_inquiry_returns_string_list_searchable_type():
    field_type = MockTypeInformation(List[str])
    inquiry_type = determine_expected_inquiry(
        True, False, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.STRING_LIST_SEARCHABLE


def test_determine_expected_inquiry_returns_enum_type():
    field_type = MockTypeInformation(TestEnum)
    inquiry_type = determine_expected_inquiry(False, True, field_type, {})
    assert inquiry_type == InquiryType.ENUM


def test_determine_expected_inquiry_returns_enum_searchable_type():
    field_type = MockTypeInformation(TestEnum)
    inquiry_type = determine_expected_inquiry(
        False, True, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.ENUM_SEARCHABLE


def test_determine_expected_inquiry_returns_enum_list_type():
    field_type = MockTypeInformation(List[TestEnum])
    inquiry_type = determine_expected_inquiry(True, True, field_type, {})
    assert inquiry_type == InquiryType.ENUM_LIST


def test_determine_expected_inquiry_returns_enum_list_searchable_type():
    field_type = MockTypeInformation(List[TestEnum])
    inquiry_type = determine_expected_inquiry(
        True, True, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.ENUM_LIST_SEARCHABLE


def test_determine_expected_inquiry_returns_path_type():
    field_type = MockTypeInformation(Path)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.PATH


def test_determine_expected_inquiry_returns_path_searchable_type():
    field_type = MockTypeInformation(Path)
    inquiry_type = determine_expected_inquiry(
        False, False, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.PATH_SEARCHABLE


def test_determine_expected_inquiry_returns_boolean_type():
    field_type = MockTypeInformation(bool)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.BOOLEAN


def test_determine_expected_inquiry_returns_int_type():
    field_type = MockTypeInformation(int)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.INT


def test_determine_expected_inquiry_returns_float_type():
    field_type = MockTypeInformation(float)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.FLOAT


def test_determine_expected_inquiry_returns_secret_type():
    field_type = MockTypeInformation(str)
    inquiry_type = determine_expected_inquiry(
        False, False, field_type, {"secret": True}
    )
    assert inquiry_type == InquiryType.SECRET

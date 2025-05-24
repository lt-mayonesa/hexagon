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


def test_determine_expected_inquiry_returns_string_type_for_str_field():
    """
    Given a field type information with base_type=str.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=False, and no special options.
    Then InquiryType.STRING should be returned.
    """
    field_type = MockTypeInformation(str)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.STRING


def test_determine_expected_inquiry_returns_string_searchable_type_when_searchable_option_is_true():
    """
    Given a field type information with base_type=str.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=False, and searchable=True.
    Then InquiryType.STRING_SEARCHABLE should be returned.
    """
    field_type = MockTypeInformation(str)
    inquiry_type = determine_expected_inquiry(
        False, False, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.STRING_SEARCHABLE


def test_determine_expected_inquiry_returns_string_list_type_for_list_str_field():
    """
    Given a field type information with base_type=List[str].
    When determine_expected_inquiry is called with is_iterable=True, is_enum=False, and no special options.
    Then InquiryType.STRING_LIST should be returned.
    """
    field_type = MockTypeInformation(List[str])
    inquiry_type = determine_expected_inquiry(True, False, field_type, {})
    assert inquiry_type == InquiryType.STRING_LIST


def test_determine_expected_inquiry_returns_string_list_searchable_type_when_searchable_option_is_true():
    """
    Given a field type information with base_type=List[str].
    When determine_expected_inquiry is called with is_iterable=True, is_enum=False, and searchable=True.
    Then InquiryType.STRING_LIST_SEARCHABLE should be returned.
    """
    field_type = MockTypeInformation(List[str])
    inquiry_type = determine_expected_inquiry(
        True, False, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.STRING_LIST_SEARCHABLE


def test_determine_expected_inquiry_returns_enum_type_for_enum_field():
    """
    Given a field type information with base_type=TestEnum.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=True, and no special options.
    Then InquiryType.ENUM should be returned.
    """
    field_type = MockTypeInformation(TestEnum)
    inquiry_type = determine_expected_inquiry(False, True, field_type, {})
    assert inquiry_type == InquiryType.ENUM


def test_determine_expected_inquiry_returns_enum_searchable_type_when_searchable_option_is_true():
    """
    Given a field type information with base_type=TestEnum.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=True, and searchable=True.
    Then InquiryType.ENUM_SEARCHABLE should be returned.
    """
    field_type = MockTypeInformation(TestEnum)
    inquiry_type = determine_expected_inquiry(
        False, True, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.ENUM_SEARCHABLE


def test_determine_expected_inquiry_returns_enum_list_type_for_list_enum_field():
    """
    Given a field type information with base_type=List[TestEnum].
    When determine_expected_inquiry is called with is_iterable=True, is_enum=True, and no special options.
    Then InquiryType.ENUM_LIST should be returned.
    """
    field_type = MockTypeInformation(List[TestEnum])
    inquiry_type = determine_expected_inquiry(True, True, field_type, {})
    assert inquiry_type == InquiryType.ENUM_LIST


def test_determine_expected_inquiry_returns_enum_list_searchable_type_when_searchable_option_is_true():
    """
    Given a field type information with base_type=List[TestEnum].
    When determine_expected_inquiry is called with is_iterable=True, is_enum=True, and searchable=True.
    Then InquiryType.ENUM_LIST_SEARCHABLE should be returned.
    """
    field_type = MockTypeInformation(List[TestEnum])
    inquiry_type = determine_expected_inquiry(
        True, True, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.ENUM_LIST_SEARCHABLE


def test_determine_expected_inquiry_returns_path_type_for_path_field():
    """
    Given a field type information with base_type=Path.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=False, and no special options.
    Then InquiryType.PATH should be returned.
    """
    field_type = MockTypeInformation(Path)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.PATH


def test_determine_expected_inquiry_returns_path_searchable_type_when_searchable_option_is_true():
    """
    Given a field type information with base_type=Path.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=False, and searchable=True.
    Then InquiryType.PATH_SEARCHABLE should be returned.
    """
    field_type = MockTypeInformation(Path)
    inquiry_type = determine_expected_inquiry(
        False, False, field_type, {"searchable": True}
    )
    assert inquiry_type == InquiryType.PATH_SEARCHABLE


def test_determine_expected_inquiry_returns_boolean_type_for_bool_field():
    """
    Given a field type information with base_type=bool.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=False, and no special options.
    Then InquiryType.BOOLEAN should be returned.
    """
    field_type = MockTypeInformation(bool)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.BOOLEAN


def test_determine_expected_inquiry_returns_int_type_for_int_field():
    """
    Given a field type information with base_type=int.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=False, and no special options.
    Then InquiryType.INT should be returned.
    """
    field_type = MockTypeInformation(int)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.INT


def test_determine_expected_inquiry_returns_float_type_for_float_field():
    """
    Given a field type information with base_type=float.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=False, and no special options.
    Then InquiryType.FLOAT should be returned.
    """
    field_type = MockTypeInformation(float)
    inquiry_type = determine_expected_inquiry(False, False, field_type, {})
    assert inquiry_type == InquiryType.FLOAT


def test_determine_expected_inquiry_returns_secret_type_when_secret_option_is_true():
    """
    Given a field type information with base_type=str.
    When determine_expected_inquiry is called with is_iterable=False, is_enum=False, and secret=True.
    Then InquiryType.SECRET should be returned.
    """
    field_type = MockTypeInformation(str)
    inquiry_type = determine_expected_inquiry(
        False, False, field_type, {"secret": True}
    )
    assert inquiry_type == InquiryType.SECRET

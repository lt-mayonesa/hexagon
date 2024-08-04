from enum import Enum
from pathlib import Path
from typing import List, Set, Optional, Dict, Union, Any, Annotated

import pytest
from pydantic import BaseModel, DirectoryPath as PydanticDirectoryPath
from pydantic.types import PathType

from hexagon.domain.hexagon_error import HexagonError
from hexagon.support.input.args import PositionalArg, OptionalArg
from hexagon.support.input.types import DirectoryPath
from hexagon.typing import should_support_multiple_args, field_type_information


@pytest.mark.parametrize(
    "field,expected",
    [
        ("name", False),
        ("last_names", True),
        ("age", False),
        ("friends", True),
        ("enemies", True),
        ("relatives", True),
        ("parents", True),
        ("grand_parents", True),
    ],
)
def test_get_generic_type_hint(field, expected):
    class TestModel(BaseModel):
        name: PositionalArg[str] = None
        last_names: PositionalArg[List[str]] = None
        age: OptionalArg[int] = None
        friends: OptionalArg[List[int]] = None
        enemies: OptionalArg[Set[int]] = None
        relatives: OptionalArg[set] = None
        parents: OptionalArg[tuple] = None
        grand_parents: Optional[OptionalArg[tuple]] = None

    model = TestModel()

    assert should_support_multiple_args(model.model_fields[field]) is expected


class Country(str, Enum):
    BRAZIL = "Brazil"
    USA = "USA"
    CANADA = "Canada"


class Pet(BaseModel):
    name: str


@pytest.mark.parametrize(
    "field,expected_type,expected_iterable,expected_of_enum",
    [
        ("name", str, False, False),
        ("last_names", List[str], True, False),
        ("age", int, False, False),
        ("friends", List[int], True, False),
        ("enemies", Set[int], True, False),
        ("relatives", set, True, False),
        ("parents", tuple, True, False),
        ("grand_parents", tuple, True, False),
        ("great_grand_parents", tuple, True, False),
        ("country", Country, False, True),
        ("countries", List[Country], True, True),
        ("pets", Dict[str, Pet], False, False),
        ("random", int, False, False),
        ("random_list", List[int], True, False),
        ("nested", Dict[str, int], False, False),
        ("file", Path, False, False),
        ("file_hexagon", Path, False, False),
    ],
)
def test_field_info(field, expected_type, expected_iterable, expected_of_enum):
    class TestModel(BaseModel):
        model_config = {"arbitrary_types_allowed": True}
        name: PositionalArg[str] = None
        last_names: PositionalArg[List[str]] = None
        age: OptionalArg[int] = None
        friends: OptionalArg[List[int]] = None
        enemies: OptionalArg[Set[int]] = None
        relatives: OptionalArg[set] = None
        parents: OptionalArg[tuple] = None
        grand_parents: Optional[OptionalArg[tuple]] = None
        great_grand_parents: OptionalArg[Optional[tuple]] = None
        country: OptionalArg[Country] = None
        countries: OptionalArg[List[Country]] = None
        pets: OptionalArg[Dict[str, Pet]] = None
        random: int = None
        random_list: List[int] = None
        nested: Optional[Dict[str, int]] = None
        file: OptionalArg[PydanticDirectoryPath] = None
        file_hexagon: OptionalArg[DirectoryPath] = None

    model = TestModel()
    type_, iterable, of_enum = field_type_information(model.model_fields[field])

    assert type_.base_type == expected_type
    assert iterable == expected_iterable
    assert of_enum == expected_of_enum


@pytest.mark.parametrize(
    "field",
    [
        "optional_arg_union",
        "arg_basic",
    ],
)
def test_field_with_multiple_types_should_raise_error(field):
    class TestModel(BaseModel):
        optional_arg_union: OptionalArg[Union[str, int]] = None
        arg_basic: Union[List[str], Dict[str, int], Any] = None

    model = TestModel()

    with pytest.raises(HexagonError):
        field_type_information(model.model_fields[field])

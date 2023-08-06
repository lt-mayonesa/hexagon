from enum import Enum
from typing import Any, Dict, Generic, TypeVar


class SelectionType(Enum):
    prompt = "prompt"
    args = "args"


SelectedObject = TypeVar("SelectedObject")


class Selection(Generic[SelectedObject]):
    def __init__(self, selected: SelectedObject, type: SelectionType, **kwargs) -> None:
        self.selected = selected
        self.type = type
        self.additional_data = kwargs

    type: SelectionType
    selected: SelectedObject
    additional_data: Dict[str, Any]

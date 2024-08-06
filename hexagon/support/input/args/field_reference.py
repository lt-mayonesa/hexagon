import dataclasses

from pydantic.fields import FieldInfo


@dataclasses.dataclass
class FieldReference:
    name: str
    info: FieldInfo

from enum import Enum
from typing import Optional, Dict, Any

from pydantic import BaseModel


class ToolType(str, Enum):
    misc = "misc"
    web = "web"
    shell = "shell"
    hexagon = "hexagon"


class Tool(BaseModel):
    name: str
    action: str
    type: ToolType = ToolType.misc
    alias: Optional[str] = None
    long_name: Optional[str] = None
    description: Optional[str] = None
    envs: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True

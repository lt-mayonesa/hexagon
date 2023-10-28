from __future__ import annotations

from enum import Enum
from typing import Callable, List, Optional, Dict, Any, Union

from pydantic import BaseModel


class ToolType(str, Enum):
    misc = "misc"
    web = "web"
    shell = "shell"
    hexagon = "hexagon"
    group = "group"
    function = "function"


class Tool(BaseModel):
    name: str
    type: ToolType = ToolType.misc
    icon: Optional[str] = None
    alias: Optional[str] = None
    long_name: Optional[str] = None
    description: Optional[str] = None
    envs: Optional[Dict[str, Any]] = None
    traced: Optional[bool] = True

    class Config:
        use_enum_values = True


class ActionTool(Tool):
    action: Union[str, List[str]]

    @property
    def executable_str(self):
        if isinstance(self.action, list):
            return "\n".join(self.action)
        cmd = str(self.action)
        return cmd[:-1] if cmd.endswith("\n") else cmd


class FunctionTool(Tool):
    function: Callable


class GroupTool(Tool):
    tools: Union[str, List[Union[ActionTool, GroupTool]]]


GroupTool.update_forward_refs()


class ToolGroupConfigFile(BaseModel):
    tools: List[Union[ActionTool, GroupTool, FunctionTool]]

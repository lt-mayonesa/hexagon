from typing import Any, List

from hexagon.domain.tool import Tool
from hexagon.domain.env import Env


class ToolExecutionParameters:
    def __init__(
        self, tool: Tool, parameters: Any, env: Env, arguments: List[object]
    ) -> None:
        self.tool = tool
        self.parameters = parameters
        self.env = env
        self.arguments = arguments

    tool: Tool
    parameters: Any
    env: Env
    arguments: List[object]
    custom_tools_path: str


class ToolExecutionData:
    def __init__(self, tool: Tool, duration: float) -> None:
        self.tool = tool
        self.duration = duration

    tool: Tool
    duration: float

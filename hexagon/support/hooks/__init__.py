from hexagon.domain.env import Env
from hexagon.domain.hooks.execution import ToolExecutionParameters, ToolExecutionData
from hexagon.domain.hooks.wax import Selection
from hexagon.domain.tool import Tool
from hexagon.support.hooks.hook import Hook


class HexagonHooks:
    start = Hook[None]("start")
    tool_selected = Hook[Selection[Tool]]("tool_selected")
    env_selected = Hook[Selection[Env]]("env_selected")
    before_tool_executed = Hook[ToolExecutionParameters]("before_tool_executed")
    tool_executed = Hook[ToolExecutionData]("tool_executed")
    end = Hook[None]("end")

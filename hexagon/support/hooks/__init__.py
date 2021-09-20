from hexagon.support.hooks.hook import Hook
from hexagon.domain.tool import Tool
from hexagon.domain.env import Env
from hexagon.domain.wax import Selection
from hexagon.domain.tool.execution import ToolExecutionParamters, ToolExecutionData


class HexagonHooks:
    start = Hook[None]("start")
    tool_selected = Hook[Selection[Tool]]("tool_selected")
    env_selected = Hook[Selection[Env]]("env_selected")
    before_tool_executed = Hook[ToolExecutionParamters]("before_tool_executed")
    tool_executed = Hook[ToolExecutionData]("tool_executed")
    end = Hook[None]("end")

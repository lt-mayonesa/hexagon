import time

from hexagon.domain.env import Env
from hexagon.domain.hooks.execution import ToolExecutionData
from hexagon.domain.tool import ActionTool
from hexagon.support.hooks import HexagonHooks


def execution_hook(func):
    """
    Decorator to add a hook to a tool execution, it will be called before and after the tool execution.

    :return: a wrapper for the decorated function
    """

    def wrapper(tool: ActionTool, env_args, env: Env, args):
        start = time.time()
        result = func(tool, env_args, env, args)
        HexagonHooks.tool_executed.run(
            ToolExecutionData(
                tool=tool, tool_env_args=env_args, duration=(time.time() - start)
            )
        )
        return result

    return wrapper

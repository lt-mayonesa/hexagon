import time

from hexagon.domain.env import Env
from hexagon.domain.tool import ActionTool
from hexagon.domain.tool.execution import ToolExecutionData
from hexagon.support.hooks import HexagonHooks


def execution_hook():
    """
    Decorator to add a hook to a tool execution, it will be called before and after the tool execution.

    :return: a wrapper for the decorated function
    """

    def decorator(func):
        def wrapper(tool: ActionTool, env_args, env: Env, args, custom_tools_path=None):
            start = time.time()
            result = func(tool, env_args, env, args, custom_tools_path)
            HexagonHooks.tool_executed.run(
                ToolExecutionData(
                    tool=tool, tool_env_args=env_args, duration=(time.time() - start)
                )
            )
            return result

        return wrapper

    return decorator

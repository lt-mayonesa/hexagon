import sys
from typing import List, Union

from hexagon.domain.env import Env
from hexagon.domain.tool import ToolType, ActionTool, GroupTool


class Tracer:
    def __init__(self, initial_trace):
        self.initial_trace = initial_trace
        self.trace = []

    def tracing(self, what: str):
        if what:
            self.trace.append(what)
        return what

    def remove_last(self):
        del self.trace[-1]

    def command(self):
        return " ".join(self.trace)

    def command_as_aliases(
        self, tools: List[Union[ActionTool, GroupTool]], envs: List[Env]
    ):
        if len(self.trace) < 1:
            return ""

        first_arg = self.trace[:1][0]

        _tool = next((t for t in tools if t.name == first_arg), None)
        if not _tool:
            return None

        aliases = self.__collect_aliases(_tool, envs)

        return " ".join([_tool.alias or _tool.name] + aliases)

    def __collect_aliases(self, _tool, envs):
        _t = _tool
        aliases = []
        for trace in self.trace[1:]:
            _env_alias = next(([x.alias] for x in envs if x.name == trace), [])
            if not _env_alias and _t.type == ToolType.group:
                _t = next((x for x in _t.tools if x.name == trace), None)
                _env_alias = [_t.alias]

            aliases += _env_alias or [trace]
        return aliases

    def has_traced(self):
        return len(self.trace) > len(self.initial_trace)


tracer = Tracer(sys.argv[1:])

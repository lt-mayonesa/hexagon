import sys
from typing import List

from hexagon.domain.env import Env
from hexagon.domain.tool import Tool


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

    def command_as_aliases(self, tools: List[Tool], envs: List[Env]):
        if len(self.trace) < 1:
            return ""

        _tool_alias = next(
            (t.alias for t in tools if t.name == self.trace[:1][0]), None
        )
        if not _tool_alias:
            return None

        try:
            al = next((x.alias for x in envs if x.name == self.trace[1:2][0]), "")
            _env_alias = [al] if al else []
        except IndexError:
            _env_alias = []
        return " ".join(
            [_tool_alias] + _env_alias + (self.trace[2 if _env_alias else 1 :])
        )

    def has_traced(self):
        return len(self.trace) > len(self.initial_trace)


tracer = Tracer(sys.argv[1:])

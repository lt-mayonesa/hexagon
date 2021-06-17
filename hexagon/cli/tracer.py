import sys


class Tracer:

    def __init__(self, initial_trace):
        self.initial_trace = initial_trace
        self.trace = []

    def tracing(self, what):
        if what:
            self.trace.append(what)
        return what

    def command(self):
        return " ".join(self.trace)

    def command_as_aliases(self, tools_dict: dict, envs_dict: dict):
        if len(self.trace) < 1:
            return ""

        _tool_alias = tools_dict[self.trace[:1][0]]["alias"]
        try:
            al = envs_dict.get(self.trace[1:2][0], {}).get("alias")
            _env_alias = [al] if al else []
        except IndexError:
            _env_alias = []
        return " ".join([_tool_alias] + _env_alias + (self.trace[2 if _env_alias else 1:]))

    def has_traced(self):
        return len(self.trace) > len(self.initial_trace)


tracer = Tracer(sys.argv[1:])

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
        if len(self.trace) <= 2:
            return ""

        tool_alias_ = tools_dict[self.trace[:1][0]]["alias"]
        env_alias_ = [envs_dict[self.trace[1:2][0]]["alias"]] if len(self.trace) > 1 else []
        return " ".join([tool_alias_] + env_alias_ + (self.trace[2:]))

    def has_traced(self):
        return len(self.trace) > len(self.initial_trace)


tracer = Tracer(sys.argv[1:])

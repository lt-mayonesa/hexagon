from typing import List, Union

from hexagon.domain.env import Env
from hexagon.domain.tool import ToolType, ActionTool, GroupTool
from hexagon.support.parse_args import CliArgs


class Tracer:
    def __init__(self, initial_cli_args: CliArgs):
        self._initial_args = initial_cli_args
        # TODO: store PositionalArg and OptionalArg in trace instead of strings
        self._trace = []

    def tracing(self, arg: Union[str, list], key: str = None):
        if arg:
            if key:
                for val in arg if isinstance(arg, list) else [arg]:
                    self._trace.append(CliArgs.key_value_arg(key, val))
            else:
                self._trace.append(arg)
        return arg

    def remove_last(self):
        del self._trace[-1]

    def trace(self):
        return " ".join([str(x) for x in self._trace])

    def aliases_trace(self, tools: List[Union[ActionTool, GroupTool]], envs: List[Env]):
        if len(self._trace) < 1:
            return ""

        first_arg = self._trace[:1][0]

        _tool = next((t for t in tools if t.name == first_arg), None)
        if not _tool:
            return None

        aliases = self.__collect_aliases(_tool, envs)

        return " ".join([_tool.alias or _tool.name] + aliases)

    def print_run_again(
        self,
        cli_command: str,
        tools: List[Union[ActionTool, GroupTool]],
        envs: List[Env],
        logger,
    ):
        if self.has_traced():
            command, aliases_command = self.trace(), self.aliases_trace(tools, envs)
            logger.extra(
                _("msg.main.tracer.run_again").format(
                    command=f"{cli_command} {command}"
                )
            )
            if aliases_command and command != aliases_command:
                logger.extra(
                    _("msg.main.tracer.or").format(
                        command=f"{cli_command} {aliases_command}"
                    )
                )

    def __collect_aliases(self, _tool, envs):
        _t = _tool
        aliases = []
        for trace in self._trace[1:]:
            _env_alias = next(([x.alias] for x in envs if x.name == trace), [])
            if not _env_alias and _t.type == ToolType.group:
                _t = next((x for x in _t.tools if x.name == trace), None)
                if _t and _t.alias:
                    _env_alias = [_t.alias]

            aliases += _env_alias or [trace]
        return [str(a) for a in aliases]

    def has_traced(self):
        return (
            len([x for x in self._trace if x not in self._initial_args.as_list()]) > 0
        )


_tracer = None


def tracer():
    global _tracer
    if not _tracer:
        raise Exception("Tracer not initialized")
    return _tracer


def init_tracer(args: CliArgs):
    global _tracer
    _tracer = Tracer(args)
    return _tracer

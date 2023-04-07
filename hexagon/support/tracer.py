from dataclasses import dataclass
from typing import List, Union, Optional

from hexagon.support.parse_args import CliArgs


@dataclass
class Trace:
    value: str
    value_alias: str
    key: str
    key_alias: str

    def real(self):
        if self.key:
            return f"{self.key}={self.value}"
        return str(self.value)

    def alias(self):
        if self.key_alias:
            return f"{self.key_alias}={self.value}"
        if self.key:
            return f"{self.key}={self.value}"
        return str(self.value_alias or self.value)


class Tracer:
    def __init__(self, initial_cli_args: CliArgs):
        self._initial_args = initial_cli_args
        self._trace: List[Trace] = []

    def tracing(
        self,
        value: Union[str, list],
        key: str = None,
        value_alias: str = None,
        key_alias: str = None,
    ):
        if value:
            if key:
                for val in value if isinstance(value, list) else [value]:
                    self._trace.append(Trace(val, value_alias, key, key_alias))
            else:
                self._trace.append(Trace(value, value_alias, key, key_alias))
        return value

    def remove_last(self):
        del self._trace[-1]

    def trace(self):
        return " ".join([x.real() for x in self._trace])

    def aliases_trace(self):
        return " ".join([x.alias() for x in self._trace])

    def print_run_again(
        self,
        cli_command: str,
        logger,
    ):
        if self.has_traced():
            command, aliases_command = self.trace(), self.aliases_trace()
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

    def has_traced(self):
        if len(self._trace) == 0:
            return False

        if len(self._trace) > self._initial_args.count():
            return True

        input_args = self._initial_args.as_str()
        matches = []
        for x in self._trace:
            if x.real() in input_args:
                matches.append(x.real())
            elif x.alias() in input_args:
                matches.append(x.alias())
            elif (
                x.real().replace("=", " ") in input_args
                or x.alias().replace("=", " ") in input_args
            ):
                matches.append(x.alias().replace("=", ""))

        return len(matches) > self._initial_args.count()


_tracer: Optional[Tracer] = None


def tracer() -> Tracer:
    global _tracer
    if not _tracer:
        raise Exception("Tracer not initialized")
    return _tracer


def init_tracer(args: CliArgs):
    global _tracer
    _tracer = Tracer(args)
    return _tracer

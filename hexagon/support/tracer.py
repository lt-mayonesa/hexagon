from dataclasses import dataclass
from enum import Enum
from typing import List, Union, Optional

from hexagon.support.input.args import CliArgs


@dataclass
class Trace:
    ref: str
    value: str
    value_alias: str
    key: str
    key_alias: str

    def real(self):
        if self.key:
            return f"{self.key}={self.__safe_value}"
        return str(self.__safe_value)

    def alias(self):
        if self.key_alias:
            return f"{self.key_alias}={self.__safe_value}"
        if self.key:
            return f"{self.key}={self.__safe_value}"
        return str(self.value_alias or self.__safe_value)

    @property
    def __safe_value(self):
        """
        if value has spaces, wrap it in quotes to avoid parsing issues in the shell
        if value has single or double quotes, use the opposite to wrap it
        let's hope for the best
        """
        if " " in self.value:
            if '"' in self.value:
                return f"'{self.value}'"
            return f'"{self.value}"'
        return self.value


class Tracer:
    def __init__(self, initial_cli_args: CliArgs):
        self._initial_args = initial_cli_args
        self._trace: List[Trace] = []

    def tracing(
        self,
        ref: str,
        value: Union[str, Enum, list, bool],
        key: str = None,
        value_alias: str = None,
        key_alias: str = None,
    ):
        if not value:
            pass

        for t in self._trace:
            if t.ref == ref:
                self._trace.remove(t)

        def to_str(v):
            if isinstance(v, Enum):
                return str(v.value)
            elif isinstance(v, bool):
                return str(v).lower()
            return str(v)

        if not key:
            self._trace.append(Trace(ref, to_str(value), value_alias, key, key_alias))
            return value

        if isinstance(value, list):
            for val in value:
                self._trace.append(Trace(ref, to_str(val), value_alias, key, key_alias))
        else:
            self._trace.append(Trace(ref, to_str(value), value_alias, key, key_alias))
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
        raise ValueError("Tracer not initialized")
    return _tracer


def init_tracer(args: CliArgs):
    global _tracer
    _tracer = Tracer(args)
    return _tracer

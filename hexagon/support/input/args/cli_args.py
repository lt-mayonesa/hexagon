from typing import Optional, Dict, Union

from hexagon.support.input.args.hexagon_args import PositionalArg
from hexagon.support.input.args.tool_args import ToolArgs


class CliArgs(ToolArgs):
    model_config = {
        **ToolArgs.model_config,
        # tool/env are part of a hierarchical selection path: each group nesting
        # level creates a new CliArgs instance, all sharing the same global Tracer.
        # Auto-tracing with a fixed ref (e.g. "arg_tool") would cause inner levels
        # to overwrite outer ones.  Tracing is handled explicitly in
        # select_and_execute_tool using a group_ref counter for unique keys.
        "trace_on_access": False,
        "trace_on_prompt": False,
    }

    show_version: bool = False
    tool: PositionalArg[Optional[str]] = None
    env: PositionalArg[Optional[str]] = None
    # extra_args typed with float in addition to ToolArgs' int for CLI numeric args
    extra_args: Optional[Dict[str, Union[list, bool, int, float, str]]] = None
    total_args: int

    # show_help, raw_extra_args inherited from ToolArgs

    def as_list(self):
        tool_val = self.tool and self.tool.value
        env_val = self.env and self.env.value
        return [str(x) for x in [tool_val, env_val] if x] + (
            self.raw_extra_args if self.raw_extra_args else []
        )

    def as_str(self):
        return " ".join(self.as_list())

    def count(self):
        return self.total_args

    @staticmethod
    def key_value_arg(key, arg):
        return f"{key}={arg}"

    @property
    def format_friendly_extra_args(self):
        return (
            {
                "positional": sorted(
                    [v for k, v in self.extra_args.items() if k.isdigit()]
                ),
                "optional": {
                    k: v for k, v in self.extra_args.items() if not k.isdigit()
                },
            }
            if self.extra_args
            else {}
        )

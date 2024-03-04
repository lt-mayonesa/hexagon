from typing import Optional, Dict, Union, List

from pydantic import BaseModel

from hexagon.support.input.args.hexagon_args import PositionalArg


class CliArgs(BaseModel):
    show_help: bool = False
    tool: PositionalArg[Optional[str]] = None
    env: PositionalArg[Optional[str]] = None

    extra_args: Optional[Dict[str, Union[list, bool, int, str]]] = None
    raw_extra_args: Optional[List[str]] = None
    total_args: int

    def as_list(self):
        return [str(x) for x in [self.tool, self.env] if x] + (
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

from enum import Enum

from hexagon.runtime.configuration import ConfigFile
from hexagon.support.input.args import ToolArgs, OptionalArg, Arg
from hexagon.support.input.types import FilePath
from hexagon.support.output.printer import log


class Target(Enum):
    STDOUT = "stdout"
    FILE = "file"


class Args(ToolArgs):
    target: OptionalArg[Target] = Arg(
        None, prompt_message="How do you want to output the schema?"
    )
    file_path: OptionalArg[FilePath] = Arg(
        None,
        prompt_message="Where do you want to save the schema?",
        allow_nonexistent=True,
    )


def main(tool, env, env_args, cli_args):
    if not cli_args.target.value:
        cli_args.target.prompt()

    if cli_args.target.value == Target.STDOUT:
        log.example(ConfigFile.schema_json(indent=2), syntax="json")
    else:
        if not cli_args.file_path.value:
            cli_args.file_path.prompt()
        with open(cli_args.file_path.value, "w") as schema_file:
            schema_file.write(ConfigFile.schema_json(indent=2))

        log.result(f"[green]Schema saved to [b]{cli_args.file_path.value}[/green]")

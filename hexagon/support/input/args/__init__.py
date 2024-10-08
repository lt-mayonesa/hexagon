from typing import Optional, Union, Any, Callable, List

from pydantic.fields import (
    Field as PydanticField,
)

from hexagon.support.input.args.cli_args import CliArgs
from hexagon.support.input.args.hexagon_args import (
    ARGUMENT_KEY_PREFIX,
    HexagonArg,
    PositionalArg,
    OptionalArg,
)
from hexagon.support.input.args.tool_args import ToolArgs

ARGUMENT_KEY_PREFIX = ARGUMENT_KEY_PREFIX
HexagonArg = HexagonArg
PositionalArg = PositionalArg
OptionalArg = OptionalArg
ToolArgs = ToolArgs
CliArgs = CliArgs


# noinspection PyPep8Naming
def Arg(
    default: Any = None,
    *,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    prompt_default: Optional[Union[Any, Callable[[Any], Any]]] = None,
    prompt_message: Optional[Union[str, Callable[[Any], str]]] = None,
    prompt_instruction: Optional[str] = None,
    prompt_suggestions: Optional[Union[List[str], Callable[[], List[str]]]] = None,
    searchable: bool = False,
    **kwargs,
):
    """
    Used to provide extra information about an argument, either for the model schema or complex validation.
    Some arguments apply only to number fields (``int``, ``float``, ``Decimal``) and some apply only to ``str``.

    TODO: add support for `validators` kwarg
    """
    kwargs.update(
        [
            (k, v)
            for k, v in {
                "prompt_default": prompt_default,
                "prompt_message": prompt_message,
                "prompt_instruction": prompt_instruction,
                "prompt_suggestions": prompt_suggestions,
                "searchable": searchable,
            }.items()
            if v is not None
        ]
    )
    return PydanticField(
        default,
        alias=alias,
        title=title,
        description=description,
        **kwargs,
    )

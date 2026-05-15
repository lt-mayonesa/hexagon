import functools
from typing import Any, Dict, List, Optional, Tuple

from hexagon.runtime.singletons import options
from hexagon.support.input.prompt.errors import AgentModeImpossibleError
from hexagon.support.input.prompt.inquiry_type import InquiryType

_BOOL_POSSIBLE_VALUES = ["true", "false"]

_SCALAR_TYPE_NAMES: Dict[InquiryType, str] = {
    InquiryType.INT: "int",
    InquiryType.FLOAT: "float",
    InquiryType.PATH: "path",
    InquiryType.SECRET: "str (secret)",
    InquiryType.STRING_LIST: "list of str",
    InquiryType.STRING: "str",
}


def _choice_values_for_inquiry(
    inquiry_type: InquiryType,
    extras: Dict[str, Any],
    field_type: Any,
) -> Optional[List[str]]:
    """Return the selectable values for choice-based inquiry types, or None."""
    if inquiry_type in (InquiryType.ENUM, InquiryType.ENUM_SEARCHABLE):
        return [e.name for e in field_type.base_type]
    if inquiry_type in (InquiryType.ENUM_LIST, InquiryType.ENUM_LIST_SEARCHABLE):
        return [e.name for e in field_type.base_type.__args__[0]]
    if inquiry_type in (
        InquiryType.STRING_SEARCHABLE,
        InquiryType.STRING_LIST_SEARCHABLE,
    ):
        raw = extras.get("choices", [])
        return [c["value"] if isinstance(c, dict) else str(c) for c in raw] or None
    if inquiry_type == InquiryType.PATH_SEARCHABLE:
        choices = extras.get("choices")
        return [str(c) for c in choices] if choices else None
    if inquiry_type == InquiryType.BOOLEAN:
        return _BOOL_POSSIBLE_VALUES
    return None


def possible_values_for_field(
    inquiry_type: InquiryType,
    extras: Dict[str, Any],
    field_type: Any,
) -> Tuple[Optional[List[str]], Optional[str]]:
    """Return ``(possible_values, expected_type)`` for a ToolArgs field prompt.

    Used to build the informative agent-mode error so the caller knows exactly
    what to supply on the next invocation.
    """
    possible_values = _choice_values_for_inquiry(inquiry_type, extras, field_type)
    if possible_values is not None:
        return possible_values, None

    if inquiry_type == InquiryType.PATH_SEARCHABLE:
        glob = extras.get("glob")
        return None, f"path (matching: {glob})" if glob else "path"

    return None, _SCALAR_TYPE_NAMES.get(inquiry_type, "str")


def _prompt_name_from_call(args: tuple, kwargs: dict) -> str:
    """Resolve the prompt label from a bound Prompt method call.

    ``for_all_methods`` binds the Prompt instance as the first element of
    ``args``.  The InquirerPy message is therefore either passed as a keyword
    argument or as the *second* positional argument (``args[1]``).
    """
    _self, *positional_prompt_args = args
    return kwargs.get("message") or (
        str(positional_prompt_args[0]) if positional_prompt_args else "prompt"
    )


def agent_mode_blocked(func):
    """Wrap a Prompt primitive so it raises :class:`AgentModeImpossibleError`
    immediately when agent mode is active.

    Used for callers of the Prompt primitives that have no corresponding CLI
    argument (e.g. internal update confirmations).  These prompts cannot be
    satisfied by providing additional CLI flags — the calling code must be
    updated to support agent mode.

    Richer, field-aware :class:`AgentModeBlockedError` errors are raised
    earlier in ``Prompt.query_field`` for ``ToolArgs`` prompt flows, where
    the agent *can* fix the problem by supplying the missing argument.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if options.agent_mode:
            raise AgentModeImpossibleError(
                prompt_message=_prompt_name_from_call(args, kwargs),
            )
        return func(*args, **kwargs)

    return wrapper

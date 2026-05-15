from enum import Enum, auto
from pathlib import Path
from unittest.mock import patch

import pytest

from hexagon.support.input.prompt.agent_mode import (
    _extract_choices_values,
    possible_values_for_field,
)
from hexagon.support.input.prompt.errors import AgentModeBlockedError
from hexagon.support.input.prompt.inquiry_type import InquiryType


# ---------------------------------------------------------------------------
# Fixtures & shared helpers
# ---------------------------------------------------------------------------


class _MockTypeInformation:
    """Minimal stand-in for hexagon.typing.TypeInformation."""

    def __init__(self, base_type, is_directory_path=False):
        self.base_type = base_type
        self.is_directory_path = is_directory_path


class _Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class _Size(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()


# ---------------------------------------------------------------------------
# AgentModeBlockedError
# ---------------------------------------------------------------------------


def test_agent_mode_blocked_error_prints_name_with_possible_values():
    """
    Given an AgentModeBlockedError with possible_values set.
    When _error_printer is called.
    Then the name and the possible values list are printed as errors.
    """
    errors_printed = []

    class _FakeLogger:
        def error(self, msg):
            errors_printed.append(msg)

    err = AgentModeBlockedError("my_field", possible_values=["a", "b", "c"])
    err.print_error(_FakeLogger())

    assert any("my_field" in m for m in errors_printed)
    assert any(all(v in m for v in ["a", "b", "c"]) for m in errors_printed)


def test_agent_mode_blocked_error_prints_name_with_expected_type():
    """
    Given an AgentModeBlockedError with expected_type set.
    When _error_printer is called.
    Then the name and the expected type are printed as errors.
    """
    errors_printed = []

    class _FakeLogger:
        def error(self, msg):
            errors_printed.append(msg)

    err = AgentModeBlockedError("my_field", expected_type="int")
    err.print_error(_FakeLogger())

    assert any("my_field" in m for m in errors_printed)
    assert any("int" in m for m in errors_printed)


def test_agent_mode_blocked_error_prints_only_name_when_no_hints():
    """
    Given an AgentModeBlockedError with neither possible_values nor expected_type.
    When _error_printer is called.
    Then only the name line is printed.
    """
    errors_printed = []

    class _FakeLogger:
        def error(self, msg):
            errors_printed.append(msg)

    err = AgentModeBlockedError("lonely_field")
    err.print_error(_FakeLogger())

    assert len(errors_printed) == 1
    assert "lonely_field" in errors_printed[0]


# ---------------------------------------------------------------------------
# _extract_choices_values
# ---------------------------------------------------------------------------


def test_extract_choices_values_handles_dict_choices():
    """
    Given a list of dict choices with 'value' keys.
    When _extract_choices_values is called.
    Then it returns a list of the 'value' strings.
    """
    choices = [{"value": "alpha", "name": "Alpha"}, {"value": "beta", "name": "Beta"}]
    result = _extract_choices_values(choices)
    assert result == ["alpha", "beta"]


def test_extract_choices_values_filters_separator_entries():
    """
    Given a list of dict choices that includes a __separator entry.
    When _extract_choices_values is called.
    Then separator entries are excluded from the result.
    """
    choices = [
        {"value": "tool-a", "name": "Tool A"},
        {"value": "__separator", "name": "---"},
        {"value": "tool-b", "name": "Tool B"},
    ]
    result = _extract_choices_values(choices)
    assert result == ["tool-a", "tool-b"]


def test_extract_choices_values_handles_plain_string_choices():
    """
    Given a list of plain string choices.
    When _extract_choices_values is called.
    Then it returns the strings as-is.
    """
    result = _extract_choices_values(["x", "y", "z"])
    assert result == ["x", "y", "z"]


def test_extract_choices_values_returns_none_for_empty_list():
    """
    Given an empty choices list.
    When _extract_choices_values is called.
    Then None is returned.
    """
    assert _extract_choices_values([]) is None


# ---------------------------------------------------------------------------
# possible_values_for_field — possible_values branch
# ---------------------------------------------------------------------------


def test_possible_values_returns_enum_names_for_enum_inquiry():
    """
    Given an ENUM inquiry type with a simple Enum field type.
    When possible_values_for_field is called.
    Then possible_values contains the enum member names and expected_type is None.
    """
    ft = _MockTypeInformation(_Color)
    pv, et = possible_values_for_field(InquiryType.ENUM, {}, ft)
    assert pv == ["RED", "GREEN", "BLUE"]
    assert et is None


def test_possible_values_returns_enum_names_for_enum_searchable_inquiry():
    """
    Given an ENUM_SEARCHABLE inquiry type.
    When possible_values_for_field is called.
    Then it behaves identically to ENUM.
    """
    ft = _MockTypeInformation(_Color)
    pv, et = possible_values_for_field(InquiryType.ENUM_SEARCHABLE, {}, ft)
    assert pv == ["RED", "GREEN", "BLUE"]
    assert et is None


def test_possible_values_returns_enum_names_for_enum_list_inquiry():
    """
    Given an ENUM_LIST inquiry type whose base_type wraps a List[Enum].
    When possible_values_for_field is called.
    Then possible_values contains the inner enum member names.
    """

    class _ListColorType:
        __args__ = [_Color]

    ft = _MockTypeInformation(_ListColorType)
    pv, et = possible_values_for_field(InquiryType.ENUM_LIST, {}, ft)
    assert pv == ["RED", "GREEN", "BLUE"]
    assert et is None


def test_possible_values_returns_choices_for_string_searchable():
    """
    Given a STRING_SEARCHABLE inquiry type and extras containing choices.
    When possible_values_for_field is called.
    Then possible_values matches the provided choices list.
    """
    ft = _MockTypeInformation(str)
    extras = {"choices": ["opt-1", "opt-2"]}
    pv, et = possible_values_for_field(InquiryType.STRING_SEARCHABLE, extras, ft)
    assert pv == ["opt-1", "opt-2"]
    assert et is None


def test_possible_values_returns_str_type_for_string_searchable_without_choices():
    """
    Given a STRING_SEARCHABLE inquiry type but no choices in extras.
    When possible_values_for_field is called.
    Then possible_values is None and expected_type is 'str'
    (free-text input with no enumerated choices).
    """
    ft = _MockTypeInformation(str)
    pv, et = possible_values_for_field(InquiryType.STRING_SEARCHABLE, {}, ft)
    assert pv is None
    assert et == "str"


def test_possible_values_returns_true_false_for_boolean():
    """
    Given a BOOLEAN inquiry type.
    When possible_values_for_field is called.
    Then possible_values is ['true', 'false'].
    """
    ft = _MockTypeInformation(bool)
    pv, et = possible_values_for_field(InquiryType.BOOLEAN, {}, ft)
    assert pv == ["true", "false"]
    assert et is None


def test_possible_values_returns_glob_hint_for_path_searchable_with_glob():
    """
    Given a PATH_SEARCHABLE inquiry type with a glob pattern in extras.
    When possible_values_for_field is called.
    Then expected_type contains the glob hint and possible_values is None.
    """
    ft = _MockTypeInformation(Path)
    extras = {"glob": "*.yaml"}
    pv, et = possible_values_for_field(InquiryType.PATH_SEARCHABLE, extras, ft)
    assert pv is None
    assert "*.yaml" in et


# ---------------------------------------------------------------------------
# possible_values_for_field — expected_type branch
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "inquiry_type, expected",
    [
        (InquiryType.INT, "int"),
        (InquiryType.FLOAT, "float"),
        (InquiryType.PATH, "path"),
        (InquiryType.SECRET, "str (secret)"),
        (InquiryType.STRING_LIST, "list of str"),
        (InquiryType.STRING, "str"),
    ],
)
def test_possible_values_returns_expected_type_for_scalar_types(inquiry_type, expected):
    """
    Given a scalar inquiry type (INT, FLOAT, PATH, SECRET, STRING_LIST, STRING).
    When possible_values_for_field is called.
    Then possible_values is None and expected_type matches the type name.
    """
    ft = _MockTypeInformation(str)
    pv, et = possible_values_for_field(inquiry_type, {}, ft)
    assert pv is None
    assert et == expected


# ---------------------------------------------------------------------------
# Prompt.query_field — agent mode guard
# ---------------------------------------------------------------------------


def test_query_field_raises_agent_mode_blocked_error_when_agent_mode_is_active():
    """
    Given agent_mode is True.
    When Prompt.query_field is called for a string field with no value.
    Then AgentModeBlockedError is raised with the field name and expected_type='str'.
    """
    from pydantic import BaseModel
    from hexagon.support.input.args import OptionalArg, Arg
    from hexagon.support.input.args.field_reference import FieldReference
    from hexagon.support.input.prompt.prompt import Prompt

    class _Model(BaseModel):
        city: OptionalArg[str] = Arg(None)

    field_ref = FieldReference("city", _Model.model_fields["city"])

    with patch("hexagon.support.input.prompt.prompt.options") as mock_opts:
        mock_opts.agent_mode = True
        mock_opts.hints_disabled = True

        with pytest.raises(AgentModeBlockedError) as exc_info:
            Prompt().query_field(field_ref, _Model)

    err = exc_info.value
    assert err.name == "city"
    assert err.expected_type == "str"
    assert err.possible_values is None


def test_query_field_raises_agent_mode_blocked_error_with_enum_choices():
    """
    Given agent_mode is True and a field typed as an Enum.
    When Prompt.query_field is called.
    Then AgentModeBlockedError is raised with possible_values listing the enum names.
    """
    from pydantic import BaseModel
    from hexagon.support.input.args import OptionalArg
    from hexagon.support.input.args.field_reference import FieldReference
    from hexagon.support.input.prompt.prompt import Prompt

    class _Model(BaseModel):
        color: OptionalArg[_Color] = None

    field_ref = FieldReference("color", _Model.model_fields["color"])

    with patch("hexagon.support.input.prompt.prompt.options") as mock_opts:
        mock_opts.agent_mode = True
        mock_opts.hints_disabled = True

        with pytest.raises(AgentModeBlockedError) as exc_info:
            Prompt().query_field(field_ref, _Model)

    err = exc_info.value
    assert err.name == "color"
    assert set(err.possible_values) == {"RED", "GREEN", "BLUE"}
    assert err.expected_type is None


def test_query_field_raises_agent_mode_blocked_error_for_boolean_field():
    """
    Given agent_mode is True and a boolean field.
    When Prompt.query_field is called.
    Then AgentModeBlockedError is raised with possible_values=['true', 'false'].
    """
    from pydantic import BaseModel
    from hexagon.support.input.args import OptionalArg
    from hexagon.support.input.args.field_reference import FieldReference
    from hexagon.support.input.prompt.prompt import Prompt

    class _Model(BaseModel):
        proceed: OptionalArg[bool] = None

    field_ref = FieldReference("proceed", _Model.model_fields["proceed"])

    with patch("hexagon.support.input.prompt.prompt.options") as mock_opts:
        mock_opts.agent_mode = True
        mock_opts.hints_disabled = True

        with pytest.raises(AgentModeBlockedError) as exc_info:
            Prompt().query_field(field_ref, _Model)

    err = exc_info.value
    assert err.name == "proceed"
    assert err.possible_values == ["true", "false"]


# ---------------------------------------------------------------------------
# Prompt low-level methods — agent mode guard (decorator path)
# ---------------------------------------------------------------------------


def test_prompt_fuzzy_raises_agent_mode_blocked_error_with_choices():
    """
    Given agent_mode is True.
    When prompt.fuzzy is called directly (as wax.py does for tool/env selection).
    Then AgentModeBlockedError is raised with the message as name and
    the choice values as possible_values.
    """
    from hexagon.support.input.prompt.prompt import Prompt

    p = Prompt()

    with patch("hexagon.support.input.prompt.agent_mode.options") as mock_opts:
        mock_opts.agent_mode = True

        with pytest.raises(AgentModeBlockedError) as exc_info:
            p.fuzzy(
                message="Hi, which tool would you like to use today?",
                choices=[
                    {"value": "deploy", "name": "Deploy"},
                    {"value": "test", "name": "Test"},
                ],
            )

    err = exc_info.value
    assert "which tool" in err.name
    assert "deploy" in err.possible_values
    assert "test" in err.possible_values


def test_prompt_text_raises_agent_mode_blocked_error():
    """
    Given agent_mode is True.
    When prompt.text is called directly.
    Then AgentModeBlockedError is raised.
    """
    from hexagon.support.input.prompt.prompt import Prompt

    p = Prompt()

    with patch("hexagon.support.input.prompt.agent_mode.options") as mock_opts:
        mock_opts.agent_mode = True

        with pytest.raises(AgentModeBlockedError) as exc_info:
            p.text(message="Enter name:")

    assert "Enter name:" in exc_info.value.name


def test_prompt_confirm_raises_agent_mode_blocked_error_with_positional_message():
    """
    Given agent_mode is True.
    When prompt.confirm is called with the message as a positional argument
    and a boolean default (the pattern used by internal tools like
    hexagon/runtime/update/hexagon.py).
    Then AgentModeBlockedError is raised with the message as name and
    possible_values=['true', 'false'].
    """
    from hexagon.support.input.prompt.prompt import Prompt

    p = Prompt()

    with patch("hexagon.support.input.prompt.agent_mode.options") as mock_opts:
        mock_opts.agent_mode = True

        with pytest.raises(AgentModeBlockedError) as exc_info:
            p.confirm("Would you like to update?", default=True)

    err = exc_info.value
    assert "Would you like to update?" in err.name
    assert err.possible_values == ["true", "false"]


def test_prompt_does_not_raise_when_agent_mode_is_false():
    """
    Given agent_mode is False.
    When prompt.fuzzy is called.
    Then AgentModeBlockedError is NOT raised (InquirerPy is invoked normally).
    """
    import sys
    from unittest.mock import MagicMock, patch

    from hexagon.support.input.prompt.prompt import Prompt  # ensure module loaded

    # Access the actual module (not the Prompt() instance set in __init__.py).
    prompt_module = sys.modules["hexagon.support.input.prompt.prompt"]

    fake_options = MagicMock()
    fake_options.agent_mode = False
    fake_options.hints_disabled = True
    fake_options.keymap.create_dir = "c-p"

    fake_inquirer = MagicMock()
    fake_inquirer.fuzzy.return_value.execute.return_value = "deploy"

    p = Prompt()

    import hexagon.support.input.prompt.agent_mode as agent_mode_module

    with (
        patch.object(agent_mode_module, "options", fake_options),
        patch.object(prompt_module, "inquirer", fake_inquirer),
    ):
        result = p.fuzzy(message="Pick tool", choices=["deploy", "test"])

    assert result == "deploy"

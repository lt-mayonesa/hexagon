import pytest

from hexagon.support.input.prompt import hints


@pytest.fixture(autouse=True)
def mock_i18n(monkeypatch):
    monkeypatch.setattr(
        hints,
        "_",
        value=translations_mock,
        raising=False,
    )
    yield


def translations_mock(msg):
    if msg == "msg.support.prompt.hints.help":
        return "help:"
    elif msg == "error.support.prompt.hints.no_hints_on_builder":
        return "HintsBuilder should have at least one hint"
    return "{keys}"


def test_hints_builder_raises_value_error_when_no_hints_added():
    """
    Given a new HintsBuilder with no hints added.
    When build() is called on the builder.
    Then a ValueError should be raised with the message 'HintsBuilder should have at least one hint'.
    """
    builder = hints.HintsBuilder()
    try:
        builder.build()
    except ValueError as e:
        assert e.args[0] == "HintsBuilder should have at least one hint"


def test_hints_builder_returns_enter_cancel_skip_hints_when_those_options_are_added():
    """
    Given a new HintsBuilder.
    When with_enter_cancel_skip() is called and then build().
    Then the result should be a formatted string containing 'ENTER / CTRL+C / CTRL+Z'.
    """
    assert hints.HintsBuilder().with_enter_cancel_skip().build() == (
        "help:\n" "ENTER / CTRL+C / CTRL+Z"
    )


def test_hints_builder_returns_autocomplete_hint_when_that_option_is_added():
    """
    Given a new HintsBuilder.
    When with_autocomplete() is called and then build().
    Then the result should be a formatted string containing 'CTRL+SPACE'.
    """
    assert hints.HintsBuilder().with_autocomplete().build() == "help:\n" "CTRL+SPACE"


def test_hints_builder_returns_select_toggle_hints_when_that_option_is_added():
    """
    Given a new HintsBuilder.
    When with_select_toggles() is called and then build().
    Then the result should be a formatted string containing all select toggle shortcuts.
    And it should include 'SPACE / CTRL+I / SHIFT+TAB / ALT+R | CTRL+R / ALT+A | CTRL+A'.
    """
    assert hints.HintsBuilder().with_select_toggles().build() == (
        "help:\n" "SPACE / CTRL+I / SHIFT+TAB / ALT+R | CTRL+R / ALT+A | CTRL+A"
    )


def test_hints_builder_returns_vertical_movement_hints_when_that_option_is_added():
    """
    Given a new HintsBuilder.
    When with_vertical_movement() is called and then build().
    Then the result should be a formatted string containing vertical movement shortcuts.
    And it should include '↓ | CTRL+N / ↑ | CTRL+P'.
    """
    assert hints.HintsBuilder().with_vertical_movement().build() == (
        "help:\n" "↓ | CTRL+N / ↑ | CTRL+P"
    )


def test_hints_builder_returns_fuzzy_toggle_hint_when_that_option_is_added():
    """
    Given a new HintsBuilder.
    When with_fuzzy_toggle() is called and then build().
    Then the result should be a formatted string containing 'CTRL+F'.
    """
    assert hints.HintsBuilder().with_fuzzy_toggle().build() == "help:\n" "CTRL+F"


def test_hints_builder_returns_all_hints_when_with_all_is_called():
    """
    Given a new HintsBuilder.
    When with_all() is called and then build().
    Then the result should be a formatted string containing all available hints.
    And the hints should be organized in a specific order across multiple lines.
    """
    assert hints.HintsBuilder().with_all().build() == (
        "help:\n"
        "CTRL+F / ↓ | CTRL+N / ↑ | CTRL+P\n"
        "SPACE / CTRL+I / SHIFT+TAB / ALT+R | CTRL+R / ALT+A | CTRL+A\n"
        "CTRL+SPACE / ENTER / CTRL+C / CTRL+Z"
    )


def test_hints_builder_returns_consistent_output_regardless_of_method_call_order():
    """
    Given a new HintsBuilder.
    When multiple hint methods are called in a different order than with_all().
    Then the result should still be the same formatted string with the same organization.
    And the hints should appear in the standard order regardless of the order they were added.
    """
    assert (
        hints.HintsBuilder()
        .with_vertical_movement()
        .with_autocomplete()
        .with_enter_cancel_skip()
        .with_fuzzy_toggle()
        .with_select_toggles()
        .build()
        == (
            "help:\n"
            "CTRL+F / ↓ | CTRL+N / ↑ | CTRL+P\n"
            "SPACE / CTRL+I / SHIFT+TAB / ALT+R | CTRL+R / ALT+A | CTRL+A\n"
            "CTRL+SPACE / ENTER / CTRL+C / CTRL+Z"
        )
    )


def test_hints_builder_deduplicates_hints_when_methods_are_called_multiple_times():
    """
    Given a new HintsBuilder.
    When the same hint methods are called multiple times in various orders.
    Then the result should still be the same formatted string as if each method was called once.
    And no duplicate hints should appear in the output.
    """
    assert (
        hints.HintsBuilder()
        .with_vertical_movement()
        .with_autocomplete()
        .with_enter_cancel_skip()
        .with_fuzzy_toggle()
        .with_select_toggles()
        .with_vertical_movement()
        .with_autocomplete()
        .with_enter_cancel_skip()
        .with_fuzzy_toggle()
        .with_select_toggles()
        .build()
        == (
            "help:\n"
            "CTRL+F / ↓ | CTRL+N / ↑ | CTRL+P\n"
            "SPACE / CTRL+I / SHIFT+TAB / ALT+R | CTRL+R / ALT+A | CTRL+A\n"
            "CTRL+SPACE / ENTER / CTRL+C / CTRL+Z"
        )
    )

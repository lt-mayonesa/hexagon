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


def test_hint_builder_no_hints():
    builder = hints.HintsBuilder()
    try:
        builder.build()
    except ValueError as e:
        assert e.args[0] == "HintsBuilder should have at least one hint"


def test_hint_builder_with_enter_cancel_skip():
    assert hints.HintsBuilder().with_enter_cancel_skip().build() == (
        "help:\n" "ENTER / CTRL+C / CTRL+Z"
    )


def test_hint_builder_with_autocomplete():
    assert hints.HintsBuilder().with_autocomplete().build() == "help:\n" "CTRL+SPACE"


def test_hint_builder_with_select_toggles():
    assert hints.HintsBuilder().with_select_toggles().build() == (
        "help:\n" "SPACE / CTRL+I / SHIFT+TAB / ALT+R | CTRL+R / ALT+A | CTRL+A"
    )


def test_hint_builder_with_vertical_movement():
    assert hints.HintsBuilder().with_vertical_movement().build() == (
        "help:\n" "↓ | CTRL+N / ↑ | CTRL+P"
    )


def test_hint_builder_with_fuzzy_toggle():
    assert hints.HintsBuilder().with_fuzzy_toggle().build() == "help:\n" "CTRL+F"


def test_hint_builder_with_all():
    assert hints.HintsBuilder().with_all().build() == (
        "help:\n"
        "CTRL+F / ↓ | CTRL+N / ↑ | CTRL+P\n"
        "SPACE / CTRL+I / SHIFT+TAB / ALT+R | CTRL+R / ALT+A | CTRL+A\n"
        "CTRL+SPACE / ENTER / CTRL+C / CTRL+Z"
    )


def test_hint_builder_with_all_in_different_order():
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


def test_hint_builder_with_all_in_different_order_and_with_duplicates():
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

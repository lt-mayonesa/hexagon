from typing import List

from hexagon.runtime.singletons import options
from hexagon.support.input.prompt.key_bindings import to_readable_name


def _fmt(msg: str, keys: List[str]) -> List[str]:
    return [msg.format(keys=" | ".join(keys))]


class HintsBuilder:
    def __init__(self):
        self.__top_hints = []
        self.__middle_hints = []
        self.__bottom_hints = []
        self.__has_enter_cancel_skip = False
        self.__has_autocomplete = False
        self.__has_select_toggles = False
        self.__has_vertical_movement = False
        self.__has_fuzzy_toggle = False
        self.__has_number_controls = False
        self.__has_floating_point = False
        self.__has_path_support = False

    def with_enter_cancel_skip(self) -> "HintsBuilder":
        if not self.__has_enter_cancel_skip:
            self.__bottom_hints += (
                _fmt(_("msg.support.prompt.hints.confirm"), ["ENTER"])
                + _fmt(_("msg.support.prompt.hints.cancel"), ["CTRL+C"])
                + _fmt(_("msg.support.prompt.hints.skip"), ["CTRL+Z"])
            )
            self.__has_enter_cancel_skip = True
        return self

    def with_autocomplete(self) -> "HintsBuilder":
        if not self.__has_autocomplete:
            self.__bottom_hints = (
                _fmt(_("msg.support.prompt.hints.autocomplete"), ["CTRL+SPACE"])
                + self.__bottom_hints
            )
            self.__has_autocomplete = True
        return self

    def with_select_toggles(self) -> "HintsBuilder":
        if not self.__has_select_toggles:
            self.__middle_hints += (
                _fmt(_("msg.support.prompt.hints.toggle"), ["SPACE"])
                + _fmt(_("msg.support.prompt.hints.toggle_move_down"), ["CTRL+I"])
                + _fmt(_("msg.support.prompt.hints.toggle_move_up"), ["SHIFT+TAB"])
                + _fmt(_("msg.support.prompt.hints.toggle_all"), ["ALT+R", "CTRL+R"])
                + _fmt(
                    _("msg.support.prompt.hints.toggle_all_true"), ["ALT+A", "CTRL+A"]
                )
            )
            self.__has_select_toggles = True
        return self

    def with_vertical_movement(self) -> "HintsBuilder":
        if not self.__has_vertical_movement:
            self.__top_hints += _fmt(
                _("msg.support.prompt.hints.move_down"), ["↓", "CTRL+N"]
            ) + _fmt(_("msg.support.prompt.hints.move_up"), ["↑", "CTRL+P"])
            self.__has_vertical_movement = True
        return self

    def with_fuzzy_toggle(self) -> "HintsBuilder":
        if not self.__has_fuzzy_toggle:
            self.__top_hints = (
                _fmt(_("msg.support.prompt.hints.toggle_fuzzy_search"), ["CTRL+F"])
                + self.__top_hints
            )
            self.__has_fuzzy_toggle = True
        return self

    def with_number_controls(self) -> "HintsBuilder":
        if not self.__has_number_controls:
            self.__top_hints += (
                _fmt(
                    _("msg.support.prompt.hints.number_decrement"),
                    ["↓", "CTRL+N"],
                )
                + _fmt(_("msg.support.prompt.hints.number_increment"), ["↑", "CTRL+P"])
                + _fmt(_("msg.support.prompt.hints.number_left"), ["←", "CTRL+B"])
                + _fmt(_("msg.support.prompt.hints.number_right"), ["→", "CTRL+F"])
            )
            self.__middle_hints = (
                _fmt(_("msg.support.prompt.hints.toggle_negative"), ["-"])
                + self.__middle_hints
            )
            self.__has_number_controls = True
        return self

    def with_floating_point(self) -> "HintsBuilder":
        if not self.__has_floating_point:
            self.__middle_hints += _fmt(
                _("msg.support.prompt.hints.number_dot"), ["."]
            ) + _fmt(
                _("msg.support.prompt.hints.alt_part_focus"), ["CTRL+I", "SHIFT+TAB"]
            )
            self.__has_floating_point = True
        return self

    def with_path_support(self) -> "HintsBuilder":
        if not self.__has_path_support:
            self.__top_hints += _fmt(
                _("msg.support.prompt.hints.create_path_at_location"),
                [to_readable_name(options.keymap.create_dir)],
            )
            self.__has_path_support = True
        return self

    def with_all(self) -> "HintsBuilder":
        return (
            self.with_enter_cancel_skip()
            .with_autocomplete()
            .with_select_toggles()
            .with_vertical_movement()
            .with_fuzzy_toggle()
        )

    def build(self) -> str:
        if not self.__top_hints and not self.__middle_hints and not self.__bottom_hints:
            raise ValueError(_("error.support.prompt.hints.no_hints_on_builder"))

        return "\n".join(
            [_("msg.support.prompt.hints.help")]
            + [
                " / ".join(line)
                for line in [self.__top_hints, self.__middle_hints, self.__bottom_hints]
                if line
            ]
        )

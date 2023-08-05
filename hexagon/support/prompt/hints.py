from typing import List


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

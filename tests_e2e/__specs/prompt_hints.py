from tests_e2e.__specs.utils.hexagon_spec import as_a_user


def test_hints_for_text_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_text"], os_env_vars={"HEXAGON_HINTS_DISABLED": "0"}
        )
        .then_output_should_be(
            [
                "Enter prompt_text",
                "help:",
                "[ CTRL+SPACE ] to autocomplete (if available) / [ ENTER ] to confirm / [ CTRL+C",
            ]
        )
        .input("foo")
        .then_output_should_be(["Enter prompt_text: foo", "result: foo"])
        .exit()
    )


def test_hints_for_multiline_text_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_text_multiline"],
            os_env_vars={"HEXAGON_HINTS_DISABLED": "0"},
        )
        .then_output_should_be(
            [
                "Enter prompt_text_multiline: (each line represents a value) ESC + Enter to fi",
                "help:",
                "[ CTRL+SPACE ] to autocomplete (if available) / [ ENTER ] to confirm / [ CTRL+C",
            ],
            discard_until_first_match=True,
        )
        .input("foo")
        .input("bar")
        .esc()
        .carriage_return()
        .then_output_should_be(
            ["Enter prompt_text_multiline: foo", "result: ['foo', 'bar']"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_hints_for_select_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_select"], os_env_vars={"HEXAGON_HINTS_DISABLED": "0"}
        )
        .then_output_should_be(
            [
                "Enter prompt_select",
                "A",
                "B",
                "C",
            ]
        )
        .carriage_return()
        .then_output_should_be(
            [
                "help:",
                "[ ↓ | CTRL+N ] to move down / [ ↑ | CTRL+P ] to move up",
                "[ ENTER ] to confirm / [ CTRL+C ] to cancel / [ CTRL+Z ] to skip",
                "result: c",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_hints_for_checkbox_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_checkbox"],
            os_env_vars={"HEXAGON_HINTS_DISABLED": "0"},
        )
        .then_output_should_be(
            [
                "Enter prompt_checkbox",
                "A",
                "B",
                "C",
            ]
        )
        .carriage_return()
        .then_output_should_be(
            [
                "help:",
                "[ ↓ | CTRL+N ] to move down / [ ↑ | CTRL+P ] to move up",
                "[ SPACE ] to toggle / [ CTRL+I ] to toggle and move down / [ SHIFT+TAB ] to tog",
                "g",
                "le and move up / [ ALT+R | CTRL+R ] to toggle all / [ ALT+A | CTRL+A ] to toggl",
                "e",
                "all to true",
                "[ ENTER ] to confirm / [ CTRL+C ] to cancel / [ CTRL+Z ] to skip",
                "result: [<Category.A: 'a'>, <Category.B: 'b'>]",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_hints_for_confirm_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_confirm"],
            os_env_vars={"HEXAGON_HINTS_DISABLED": "0"},
        )
        .then_output_should_be(["Are you sure?"])
        .carriage_return()
        .then_output_should_be(
            [
                "help:",
                "[ ENTER ] to confirm / [ CTRL+C ] to cancel / [ CTRL+Z ] to skip",
                "result: True",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_hints_for_fuzzy_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_fuzzy"],
            os_env_vars={"HEXAGON_HINTS_DISABLED": "0"},
        )
        .then_output_should_be(
            [
                "Enter prompt_fuzzy",
                "",
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
            ]
        )
        .arrow_down()
        .carriage_return()
        .then_output_should_be(
            [
                "help:",
                "[ CTRL+F ] to toggle fuzzy search / [ ↓ | CTRL+N ] to move down / [ ↑ | CTRL+P",
                "]",
                "to move up",
                "[ ENTER ] to confirm / [ CTRL+C ] to cancel / [ CTRL+Z ] to skip",
                "result: b",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_hints_for_fuzzy_multiselect_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_fuzzy_multiselect"],
            os_env_vars={"HEXAGON_HINTS_DISABLED": "0"},
        )
        .then_output_should_be(
            [
                "Enter prompt_fuzzy_multiselect",
                "",
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
            ]
        )
        .carriage_return()
        .then_output_should_be(
            [
                "help:",
                "[ CTRL+F ] to toggle fuzzy search / [ ↓ | CTRL+N ] to move down / [ ↑ | CTRL+P",
                "[ SPACE ] to toggle / [ CTRL+I ] to toggle and move down / [ SHIFT+TAB ] to tog",
                "g",
                "le and move up / [ ALT+R | CTRL+R ] to toggle all / [ ALT+A | CTRL+A ] to toggl",
                "e",
                "all to true",
                "[ ENTER ] to confirm / [ CTRL+C ] to cancel / [ CTRL+Z ] to skip",
                "result: ['a']",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_hints_for_path_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_path"],
            os_env_vars={"HEXAGON_HINTS_DISABLED": "0"},
        )
        .then_output_should_be(
            [
                "Enter prompt_path",
                "help:",
                "[ CTRL+SPACE ] to autocomplete (if available) / [ ENTER ] to confirm / [ CTRL+C",
            ]
        )
        .input("app.yml")
        .then_output_should_be(
            ["Enter prompt_path: app.yml", "result: app.yml"],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_hints_for_number_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_number"],
            os_env_vars={"HEXAGON_HINTS_DISABLED": "0"},
        )
        .input("1")
        .then_output_should_be(
            [
                "Enter prompt_number",
                "help:",
                "[ ↓ | CTRL+N ] to decrement / [ ↑ | CTRL+P ] to increment / [ ← | CTRL+B ] to s",
                "e",
                "lect number left / " "[ → | CTRL+F ] to select number right",
                "[ - ] to toggle negative",
                "[ ENTER ] to confirm / [ CTRL+C ] to cancel / [ CTRL+Z ] to skip",
                "result: 1",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_hints_for_floating_number_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_number_float"],
            os_env_vars={"HEXAGON_HINTS_DISABLED": "0"},
        )
        .input("1.23")
        .then_output_should_be(
            [
                "Enter prompt_number_float",
                "help:",
                "[ ↓ | CTRL+N ] to decrement / [ ↑ | CTRL+P ] to increment / [ ← | CTRL+B ] to s",
                "e",
                "lect number left / " "[ → | CTRL+F ] to select number right",
                "[ - ] to toggle negative / [ . ] to select decimal part / [ CTRL+I | SHIFT+TAB",
                "]",
                "to alternate focused part",
                "[ ENTER ] to confirm / [ CTRL+C ] to cancel / [ CTRL+Z ] to skip",
                "result: 1.023",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_hints_for_secret_prompt_are_generated_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["hints", "hints_secret"],
            os_env_vars={"HEXAGON_HINTS_DISABLED": "0"},
        )
        .input("foo")
        .then_output_should_be(
            [
                "Enter prompt_text_secret",
                "help:",
                [
                    "[ ENTER ] to confirm / [ CTRL+C ] to cancel / [ CTRL+Z ] to skip",
                    "Enter prompt_text_secret: ***",
                ],
                "result: foo",
            ]
        )
        .exit()
    )

from tests_e2e.framework.hexagon_spec import as_a_user


def test_show_default_when_arg_has_prompt_default():
    (
        as_a_user(__file__)
        .run_hexagon(["default-arguments", "arg_has_prompt_default"])
        .then_output_should_be(
            [
                "initial value: None",
                "Enter name: John",
            ]
        )
        .input(" Doe")
        .then_output_should_be(
            [
                "Enter name: John Doe",
                "prompt result: John Doe",
            ]
        )
        .exit()
    )


def test_show_default_when_arg_has_default():
    (
        as_a_user(__file__)
        .run_hexagon(["default-arguments", "arg_has_default"])
        .then_output_should_be(
            [
                "initial value: 23",
                "Enter age:",
            ]
        )
        .erase(2)
        .input("43")
        .then_output_should_be(
            [
                "Enter age: 43",
                "prompt result: 43",
            ]
        )
        .exit()
    )


def test_show_default_for_enum_value():
    (
        as_a_user(__file__)
        .run_hexagon(["default-arguments", "enum_default"])
        .then_output_should_be(
            [
                "initial value: None",
                "Enter category:",
                "cat",
                "dog",
                "bird",
                "❯ insect",
                "fish",
            ]
        )
        .arrow_up()
        .carriage_return()
        .then_output_should_be(
            [
                "Enter category: bird",
                "prompt result: Category.bird",
            ]
        )
        .exit()
    )


def test_show_default_for_multiselect_enum_value():
    (
        as_a_user(__file__)
        .run_hexagon(["default-arguments", "enum_multiselect"])
        .then_output_should_be(
            [
                "initial value: None",
                "Enter brands:",
                "○ ford",
                "○ fiat",
                "◉ toyota",
                "◉ renault",
            ]
        )
        .carriage_return()
        .then_output_should_be(
            [
                "Enter brands: ['toyota', 'renault']",
                "prompt result: [<Brand.toyota: 'toyota'>, <Brand.renault: 'renault'>]",
            ]
        )
        .exit()
    )

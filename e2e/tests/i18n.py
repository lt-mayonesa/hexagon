from e2e.tests.utils.hexagon_spec import as_a_user


def test_default_locale_is_english():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "",
                "",
                "⦾ Google",
                "",
                "ƒ Python i18n Test",
            ]
        )
        .then_output_should_be(
            [
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ],
            True,
        )
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "ƒ Python i18n Test"],
                "stub",
            ]
        )
        .exit()
    )


def test_fallback_locale_is_english():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"LANGUAGE": "fr"})
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "",
                "",
                "⦾ Google",
                "",
                "ƒ Python i18n Test",
            ]
        )
        .then_output_should_be(
            [
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ],
            True,
        )
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "ƒ Python i18n Test"],
                "stub",
            ]
        )
        .exit()
    )


def test_locale_is_set_to_english():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"LANGUAGE": "en"})
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "",
                "",
                "⦾ Google",
                "",
                "ƒ Python i18n Test",
            ]
        )
        .then_output_should_be(
            [
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ],
            True,
        )
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "ƒ Python i18n Test"],
                "stub",
            ]
        )
        .exit()
    )


def test_locale_is_set_to_spanish():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"LANGUAGE": "es"})
        .then_output_should_be(
            [
                "Hola ¿qué herramienta te gustaría usar hoy?",
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "",
                "",
                "⦾ Google",
                "",
                "ƒ Python i18n Test",
            ]
        )
        .then_output_should_be(
            [
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ],
            True,
        )
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                ["Hola ¿qué herramienta te gustaría usar hoy?", "ƒ Python i18n Test"],
                "stub",
            ]
        )
        .exit()
    )

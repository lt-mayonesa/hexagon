from tests_e2e.__specs.utils.hexagon_spec import as_a_user


def test_default_locale_is_english():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "4/4",
                "⦾ Google",
                "ƒ Python i18n Test",
                "⬡ Save Last Command as Shell Alias",
                "⬡ Create A New Tool",
            ]
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


def test_unknown_language_fallbacks_to_english():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"LANGUAGE": "fr"})
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "4/4",
                "⦾ Google",
                "ƒ Python i18n Test",
                "⬡ Save Last Command as Shell Alias",
                "⬡ Create A New Tool",
            ]
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


def test_not_found_locales_fallbacks_to_english():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_LOCALES_DIR": "/some/unknown/path"})
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "4/4",
                "⦾ Google",
                "ƒ Python i18n Test",
                "⬡ Save Last Command as Shell Alias",
                "⬡ Create A New Tool",
            ]
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
                "4/4",
                "⦾ Google",
                "ƒ Python i18n Test",
                "⬡ Save Last Command as Shell Alias",
                "⬡ Create A New Tool",
            ]
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
                "4/4",
                "⦾ Google",
                "ƒ Python i18n Test",
                "⬡ Guardar el último comando ejecutado como shell alias",
                "⬡ Crear una nueva herramienta",
            ]
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

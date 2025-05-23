from tests_e2e.framework.hexagon_spec import as_a_user


def test_panel_with_default_values_is_shown():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["panel", "default_args_panel"], os_env_vars={"HEXAGON_THEME": "no_border"}
        )
        .then_output_should_be(
            [
                "",
                "",
                "╭─────────────────────────╮",
                "│                         │",
                "│     This is a panel     │",
                "│                         │",
                "╰─────────────────────────╯",
            ]
        )
        .exit()
    )


def test_panel_with_title_and_footer():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["panel", "title_and_footer"], os_env_vars={"HEXAGON_THEME": "no_border"}
        )
        .then_output_should_be(
            [
                "",
                "",
                "╭───────── title ─────────╮",
                "│                         │",
                "│     This is a panel     │",
                "│                         │",
                "╰──────── footer ─────────╯",
            ]
        )
        .exit()
    )


def test_panel_unfit():
    (
        as_a_user(__file__)
        .run_hexagon(["panel", "fit_false"], os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [
                "",
                "",
                "╭─────────────────────────────────────────────────────────────────────────────────────────────── title ────────────────────────────────────────────────────────────────────────────────────────────────╮",  # noqa: E501
                "│                                                                                                                                                                                                      │",  # noqa: E501
                "│     This is a panel                                                                                                                                                                                  │",  # noqa: E501
                "│                                                                                                                                                                                                      │",  # noqa: E501
                "╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯",  # noqa: E501
            ]
        )
        .exit()
    )


def test_panel_padding_and_justify():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["panel", "padding_and_justify"], os_env_vars={"HEXAGON_THEME": "no_border"}
        )
        .then_output_should_be(
            [
                "",
                "",
                "╭───────────────────────────────────────────────╮",
                "│                                               │",
                "│                                               │",
                "│                                               │",
                "│                                               │",
                "│                This is a panel                │",
                "│  The content will be justified to the center  │",
                "│                                               │",
                "│                                               │",
                "│                                               │",
                "│                                               │",
                "╰───────────────────────────────────────────────╯",
            ]
        )
        .exit()
    )

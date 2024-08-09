from tests_e2e.__specs.utils.hexagon_spec import as_a_user


def test_text_should_be_autocompleted():
    (
        as_a_user(__file__)
        .run_hexagon(["completer"], os_env_vars={"HEXAGON_THEME": "no_border"})
        .input("tes")
        .tab()
        .arrow_down()
        .carriage_return()
        .then_output_should_be(
            [
                "test: tes",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

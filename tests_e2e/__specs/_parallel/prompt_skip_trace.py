from tests_e2e.framework.hexagon_spec import as_a_user


def test_when_trace_is_skipped_execute_again_is_not_shown():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt-skip-trace-test", "skip_trace_bool"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .input("foo")
        .then_output_should_be(
            ["Enter prompt_text: foo"], discard_until_first_match=True
        )
        .then_output_should_not_contain(["To run this tool again do:"])
        .exit()
    )


def test_when_trace_is_skipped_for_1_execute_again_is_not_show_for_that_arg():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt-skip-trace-test", "skip_trace_bool_two_args"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .input("foo")
        .then_output_should_be(
            ["Enter prompt_text: foo"], discard_until_first_match=True
        )
        .input("bar")
        .then_output_should_be(
            ["Enter prompt_text_two: bar"], discard_until_first_match=True
        )
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt-skip-trace-test skip_trace_bool_two_args --prompt-text-two=bar",
                "or:",
                "hexagon-test pstt skip_trace_bool_two_args -ptt=bar",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_trace_is_skipped_using_callable():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt-skip-trace-test", "skip_trace_callable"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .input("foo")
        .then_output_should_be(
            ["Enter prompt_text: foo"], discard_until_first_match=True
        )
        .then_output_should_not_contain(["To run this tool again do:"])
        .exit()
    )


def test_trace_is_not_skipped_when_callable_returns_falsy():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt-skip-trace-test", "skip_trace_callable_falsy"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .input("foo")
        .then_output_should_be(
            ["Enter prompt_text: foo"], discard_until_first_match=True
        )
        .input("bar")
        .then_output_should_be(
            ["Enter prompt_text: bar"], discard_until_first_match=True
        )
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt-skip-trace-test skip_trace_callable_falsy --prompt-text=foo",
                "or:",
                "hexagon-test pstt skip_trace_callable_falsy -pt=foo",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

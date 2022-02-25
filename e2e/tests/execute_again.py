from e2e.tests.utils.hexagon_spec import as_a_user


def test_command_with_alias_execute_again_is_shown():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "default"})
        .enter()
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test command-with-alias",
                "or:",
                "hexagon-test cwa",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_command_with_alias_and_env_execute_again_is_shown():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "default"})
        # select command-env-with-alias tool
        .arrow_down()
        .enter()
        # select first env
        .enter()
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test command-env-with-alias",
                "or:",
                "hexagon-test cewa",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_with_input_command_with_alias_and_env_execute_again_is_shown():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["command-env-with-alias"], os_env_vars={"HEXAGON_THEME": "default"}
        )
        # select first env
        .enter()
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test command-env-with-alias",
                "or:",
                "hexagon-test cewa",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


# noinspection PyPep8Naming
def test_WHEN_no_prompts_are_shown_THEN_execute_again_is_hidden():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["command-env-with-alias", "dev"], os_env_vars={"HEXAGON_THEME": "default"}
        )
        .then_output_should_not_contain(
            [
                "To run this tool again do:",
                "hexagon-test command-env-with-alias",
                "or:",
                "hexagon-test cewa",
            ]
        )
        .exit()
    )


# noinspection PyPep8Naming
def test_WHEN_command_with_no_alias_THEN_execute_again_is_shown_partially():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "default"})
        # select command-no-alias tool
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            ["To run this tool again do:", "hexagon-test command-no-alias"],
            discard_until_first_match=True,
        )
        .then_output_should_not_contain(["or:", "hexagon-test"])
        .exit()
    )


# noinspection PyPep8Naming
def test_WHEN_group_tool_command_is_executed_THEN_execute_again_is_shown():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "default"})
        # select command-no-alias tool
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .enter()
        .enter()
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test tool-group group-command-first",
                "or:",
                "hexagon-test tg gcf",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

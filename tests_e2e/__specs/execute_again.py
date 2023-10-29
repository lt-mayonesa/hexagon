from tests_e2e.__specs.utils.hexagon_spec import as_a_user


def test_command_with_alias_execute_again_is_shown():
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
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
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        # select command-env-with-alias tool
        .arrow_down()
        .enter()
        .then_output_should_be(
            ["This is a command with env with"], discard_until_first_match=True
        )
        .then_output_should_be(
            ["On which environment?"], discard_until_first_match=True
        )
        # select first env
        .enter()
        .then_output_should_be(["dev"], discard_until_first_match=True)
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
            ["command-env-with-alias"], os_env_vars={"HEXAGON_THEME": "no_border"}
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
            ["command-env-with-alias", "dev"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
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
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
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
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        # select command-no-alias tool
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(["tool-group"], discard_until_first_match=True)
        .then_output_should_be(
            ["Hi, which tool would you like to use today?"],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["group-command-first"], discard_until_first_match=True)
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


def test_enum_values_are_printed_not_names():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["test-enum-values"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .carriage_return()
        .then_output_should_be(
            [
                "test: Test.MY_ENUM",
                "To run this tool again do:",
                "hexagon-test test-enum-values this_should_be_printed",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

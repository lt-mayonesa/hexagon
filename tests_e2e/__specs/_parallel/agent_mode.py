"""
E2E tests for HEXAGON_AGENT_MODE=true.

When agent mode is active every interactive prompt must fail immediately
with an informative error instead of waiting for user input.  Agents are
expected to supply all required arguments up-front.
"""

from tests_e2e.framework.hexagon_spec import as_a_user

_AGENT_ENV = {"HEXAGON_AGENT_MODE": "true"}


def test_agent_mode_blocks_tool_selection_and_lists_available_tools():
    """
    Given HEXAGON_AGENT_MODE=true.
    When hexagon is invoked without specifying a tool.
    Then it exits with status 1 naming the 'tool' argument and listing
    the available tool names as possible values.
    """
    (
        as_a_user(__file__)
        .run_hexagon([], os_env_vars=_AGENT_ENV)
        .then_output_should_be(
            [
                [
                    "Agent mode is active",
                    "'tool'",
                    "requires a value but prompt is disabled",
                ]
            ],
            discard_until_first_match=True,
        )
        .then_output_should_be(
            [["Possible values:", "greet", "pick-color"]],
            discard_until_first_match=True,
        )
        .exit(status=1)
    )


def test_agent_mode_blocks_string_field_prompt_and_reports_expected_type():
    """
    Given HEXAGON_AGENT_MODE=true and the 'greet' tool is selected.
    When the tool tries to prompt for the 'name' string argument.
    Then it exits with status 1 naming the field and its expected type.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["greet"], os_env_vars=_AGENT_ENV)
        .then_output_should_be(
            [
                [
                    "Agent mode is active",
                    "'name'",
                    "requires a value but prompt is disabled",
                ]
            ],
            discard_until_first_match=True,
        )
        .then_output_should_be(
            ["Expected type: str"],
            discard_until_first_match=True,
        )
        .exit(status=1)
    )


def test_agent_mode_blocks_enum_field_prompt_and_reports_possible_values():
    """
    Given HEXAGON_AGENT_MODE=true and the 'pick-color' tool is selected.
    When the tool tries to prompt for the enum 'color' argument.
    Then it exits with status 1 naming the field and listing the enum choices.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["pick-color"], os_env_vars=_AGENT_ENV)
        .then_output_should_be(
            [
                [
                    "Agent mode is active",
                    "'color'",
                    "requires a value but prompt is disabled",
                ]
            ],
            discard_until_first_match=True,
        )
        .then_output_should_be(
            [["Possible values:", "RED", "GREEN", "BLUE"]],
            discard_until_first_match=True,
        )
        .exit(status=1)
    )


def test_agent_mode_blocks_field_with_runtime_choices_and_reports_them():
    """
    Given HEXAGON_AGENT_MODE=true and a tool that loads choices at runtime
    and passes them to .prompt(choices=[...]).
    When the tool tries to prompt for the argument.
    Then it exits with status 1 and reports the runtime-loaded choices.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["pick-option"], os_env_vars=_AGENT_ENV)
        .then_output_should_be(
            [
                [
                    "Agent mode is active",
                    "'option'",
                    "requires a value but prompt is disabled",
                ]
            ],
            discard_until_first_match=True,
        )
        .then_output_should_be(
            [["Possible values:", "fast", "slow", "medium"]],
            discard_until_first_match=True,
        )
        .exit(status=1)
    )


def test_agent_mode_raises_impossible_error_for_direct_prompt_call():
    """
    Given HEXAGON_AGENT_MODE=true and a tool that calls prompt.confirm()
    directly (not through ToolArgs), mirroring internal tools like
    hexagon/runtime/update/hexagon.py.
    When the tool reaches the confirm call.
    Then it exits with status 1 reporting the prompt message and stating
    it cannot be provided via CLI arguments.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["direct-prompt"], os_env_vars=_AGENT_ENV)
        .then_output_should_be(
            [
                [
                    "Agent mode is active",
                    "Do you want to continue?",
                    "cannot be provided via CLI arguments",
                ]
            ],
            discard_until_first_match=True,
        )
        .exit(status=1)
    )


def test_agent_mode_does_not_block_when_no_prompts_are_needed():
    """
    Given HEXAGON_AGENT_MODE=true.
    When hexagon is invoked with a tool that reads argument values directly
    (never calls .prompt()) and all arguments are provided via CLI.
    Then it runs successfully without any prompt interaction.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["greet-direct", "--name=Alice"], os_env_vars=_AGENT_ENV)
        .then_output_should_be(
            ["Hello, Alice!"],
            discard_until_first_match=True,
        )
        .exit()
    )

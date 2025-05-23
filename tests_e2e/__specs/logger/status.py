from tests_e2e.framework.hexagon_spec import as_a_user


def test_status_is_shown_correctly():
    """
    We are not actually testing the display of the spinner,
    rich hides it when not running in a TTY.
    But we are testing that status nesting and prompting works correctly.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["status"], os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            ["Test", "", "some info 1", "some info 2", "update?"],
            ignore_blank_lines=False,
        )
        .input("y")
        .then_output_should_be(
            [
                "update? Yes",
                "about to show nested status",
                "inside nested status",
                "prompting...",
                "enter something",
            ]
        )
        .input("asdf")
        .then_output_should_be(
            [
                "entered",
                "back to main status",
                "showing a new status...",
                "inside new status",
            ],
        )
        .exit(status=0)
    )

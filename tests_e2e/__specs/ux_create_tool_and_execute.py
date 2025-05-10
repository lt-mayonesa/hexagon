from tests_e2e.__specs.utils.hexagon_spec import as_a_user

LONG_NAME = "Custom Action Test"
DESCRIPTION = "Hexagon Custom Action Test Description"

config_file = {
    "cli": {"name": "Test", "command": "hexagon-test", "custom_tools_dir": "."},
    "tools": [
        {"name": "google", "long_name": "Google", "type": "web", "action": "open_link"}
    ],
    "envs": [],
}


def test_creates_a_python_tool_and_executes_it():
    spec = (
        as_a_user(__file__)
        .given_a_cli_yaml(config_file)
        .run_hexagon(["create-tool"])
        .arrow_down()
        .enter()
        .input("a_new_action")
        .then_output_should_be(
            [["What name would you like to give your new action?", "a_new_action"]],
            discard_until_first_match=True,
        )
        .carriage_return()
        .input("-command")
        .enter()
        .input(LONG_NAME)
        .input(DESCRIPTION)
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(
            ["a-new-action-command", "--last-name=my-last-name"],
            {"HEXAGON_THEME": "no_border"},
        )
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "│ selected tool: a_new_action",
                "│ selected env: None",
                "│ values in tool.envs[env.name]: None",
                "│ extra cli arguments: show_help=False extra_args=None raw_extra_args=[] last_name=",
                "├ your last name is: my-last-name",
                "│",
                "╰╼",
            ]
        )
        .exit()
    )

import os
import shutil

from e2e.tests.utils.hexagon_spec import as_a_user
from e2e.tests.utils.path import e2e_test_folder_path

LONG_NAME = "Custom Action Test"
DESCRIPTION = "Hexagon Custom Action Test Description"

config_file = {
    "cli": {"name": "Test", "command": "hexagon-test", "custom_tools_dir": "."},
    "tools": [
        {"name": "google", "long_name": "Google", "type": "web", "action": "open_link"}
    ],
    "envs": [],
}


def _clear_custom_tool():
    custom_tool_path = os.path.join(e2e_test_folder_path(__file__), "a-new-action")
    if os.path.isdir(custom_tool_path):
        shutil.rmtree(custom_tool_path)


def test_creates_a_python_tool_and_executes_it():
    _clear_custom_tool()
    (
        as_a_user(__file__)
        .given_a_cli_yaml(config_file)
        .run_hexagon(["create-tool"])
        .arrow_down()
        .arrow_down()
        .enter()
        .input("a-new-action")
        .carriage_return()
        .input("-command")
        .enter()
        .input(LONG_NAME)
        .input(DESCRIPTION)
        .exit()
    )

    (
        as_a_user(__file__)
        .run_hexagon(
            ["a-new-action-command", "env", "my-last-name"],
            {"HEXAGON_THEME": "default"},
        )
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "│ Tool.action: a-new-action",
                "│ Env: None",
                "│ Valor en tool.envs: None",
                "│ tu apellido es: my-last-name",
                "│",
                "╰╼",
            ]
        )
        .exit()
    )

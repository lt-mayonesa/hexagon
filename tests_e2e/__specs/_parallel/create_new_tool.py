import os
import shutil
from pathlib import Path

from tests_e2e.framework.config import read_hexagon_config
from tests_e2e.framework.hexagon_spec import HexagonSpec, as_a_user

LONG_NAME = "Custom Action Test"
DESCRIPTION = "Hexagon Custom Action Test Description"

base_app_file = {
    "cli": {"name": "Test", "command": "hexagon-test", "custom_tools_dir": "."},
    "tools": [
        {"name": "google", "long_name": "Google", "type": "web", "action": "open_link"}
    ],
    "envs": [],
}


def _shared_assertions(spec: HexagonSpec):
    (
        spec.then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "4/4",
                "⦾ Google",
                "⬡ Save Last Command as Shell Alias",
                "⬡ Replay Last Command",
                "⬡ Create A New Tool",
            ],
        )
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [["Hi, which tool would you like to use today?", "Create A New Tool"]],
            discard_until_first_match=True,
        )
        .then_output_should_be(
            [
                "Choose the action of your tool:",
                "2/2",
                "open_link",
                "new_action",
            ]
        )
    )


def test_create_new_open_link_tool():
    spec = (
        as_a_user(__file__)
        .given_a_cli_yaml(base_app_file)
        .run_hexagon()
        .with_shared_behavior(_shared_assertions)
        .enter()
        .then_output_should_be([["Choose the action of your tool:", "open_link"]])
        .then_output_should_be(["What type of tool is it?", "web", "shell"])
        .carriage_return()
        .then_output_should_be(
            [["What type of tool is it?", "web"]], discard_until_first_match=True
        )
        .input("-test")
        .then_output_should_be(
            [["What command would you like to give your tool?", "open-link-test"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(
            [["Would you like to add an alias/shortcut? (empty for none)", "olt"]]
        )
        .input(LONG_NAME)
        .then_output_should_be(
            [
                "Would you like to add a long name? (this will be displayed instead of command"
            ],
            discard_until_first_match=True,
        )
        .input(DESCRIPTION)
        .then_output_should_be(
            ["Would you like to add a description? (this will be displayed along side"],
            discard_until_first_match=True,
        )
        .exit()
    )

    app_file = read_hexagon_config(spec.test_dir)
    created_tool = app_file["tools"][1]
    assert created_tool["action"] == "open_link"
    assert created_tool["type"] == "web"
    assert created_tool["alias"] == "olt"


def test_create_new_python_module_tool():
    spec = (
        as_a_user(__file__)
        .given_a_cli_yaml(base_app_file)
        .run_hexagon()
        .with_shared_behavior(_shared_assertions)
        .arrow_down()
        .enter()
        .then_output_should_be([["Choose the action of your tool:", "new_action"]])
        .input("a-new-action")
        .then_output_should_be(
            [["What name would you like to give your new action?", "a-new-action"]],
            discard_until_first_match=True,
        )
        .then_output_should_be(["What type of tool is it?", "web", "shell"])
        .carriage_return()
        .then_output_should_be(
            [["What type of tool is it?", "shell"]],
            discard_until_first_match=True,
        )
        .input("-command")
        .then_output_should_be(
            [
                [
                    "What command would you like to give your tool?",
                    "a-new-action-command",
                ]
            ],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(
            [["Would you like to add an alias/shortcut? (empty for none)", "anac"]]
        )
        .input(LONG_NAME)
        .input(DESCRIPTION)
        .then_output_should_be(
            [
                "Would you like to add a long name? (this will be displayed instead of command"
            ],
            discard_until_first_match=True,
        )
        .then_output_should_be(
            ["Would you like to add a description? (this will be displayed along side"],
            True,
        )
        .exit()
    )

    app_file = read_hexagon_config(spec.test_dir)
    created_tool = app_file["tools"][1]
    assert created_tool["action"] == "a-new-action"
    assert created_tool["type"] == "shell"
    assert created_tool["alias"] == "anac"

    assert os.path.isfile(os.path.join(spec.test_dir, "a-new-action/__init__.py"))
    assert os.path.isfile(os.path.join(spec.test_dir, "a-new-action/README.md"))

    shutil.rmtree(os.path.join(spec.test_dir, "a-new-action"))


def test_create_tool_creates_custom_tools_dir():
    custom_tools_dir_name = "custom-tools-dir"
    app_file = base_app_file.copy()
    app_file["cli"].pop("custom_tools_dir")

    spec = (
        as_a_user(__file__)
        .executing_first(
            lambda spec: Path(spec.test_dir)
            .joinpath(custom_tools_dir_name)
            .mkdir(exist_ok=True, parents=True)
        )
        .given_a_cli_yaml(app_file)
        .run_hexagon()
        .with_shared_behavior(_shared_assertions)
        .arrow_down()
        .enter()
        .input("a-new-action")
        .then_output_should_be(
            ["What name would you like to give your new action? a-new-action"],
            discard_until_first_match=True,
        )
        .carriage_return()
        .input("-command")
        .enter()
        .input(LONG_NAME)
        .input(DESCRIPTION)
        .then_output_should_be(
            [
                "Where would you like it to be? (can be absolute path or relative to YAML",
                "",
            ],
            discard_until_first_match=True,
        )
        .input(f"/{custom_tools_dir_name}")
        .exit()
    )

    config_file = read_hexagon_config(spec.test_dir)

    assert config_file["cli"]["custom_tools_dir"] == f"./{custom_tools_dir_name}"

    assert os.path.isfile(
        os.path.join(spec.test_dir, custom_tools_dir_name, "a-new-action/__init__.py")
    )
    assert os.path.isfile(
        os.path.join(spec.test_dir, custom_tools_dir_name, "a-new-action/README.md")
    )

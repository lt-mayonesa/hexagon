import os
import shutil

from e2e.tests.utils.config import read_hexagon_config
from e2e.tests.utils.hexagon_spec import HexagonSpec, as_a_user
from e2e.tests.utils.path import e2e_test_folder_path

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
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "",
                "",
                "⦾ Google",
                "",
                "⬡ Save Last Command as Shell Alias",
                "",
                "⬡ Create A New Tool",
                "",
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ],
        )
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [["Hi, which tool would you like to use today?", "⬡ Create A New Tool"]]
        )
        .then_output_should_be(
            [
                "Choose the action of your tool:",
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "",
                "",
                "docker_registry",
                "",
                "open_link",
                "",
                "new_action",
                "",
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ]
        )
    )


def test_create_new_open_link_tool():
    (
        as_a_user(__file__)
        .given_a_cli_yaml(base_app_file)
        .run_hexagon()
        .with_shared_behavior(_shared_assertions)
        .arrow_down()
        .enter()
        .then_output_should_be([["Choose the action of your tool:", "open_link"]])
        .then_output_should_be(["What type of tool is it?", "web", "shell"])
        .carriage_return()
        .then_output_should_be([["What type of tool is it?", "web"]])
        .input("-test")
        .then_output_should_be(
            [["What command would you like to give your tool?", "open-link-test"]]
        )
        .enter()
        .then_output_should_be(
            [["Would you like to add an alias/shortcut? (empty for none)", "olt"]]
        )
        .input(LONG_NAME)
        .then_output_should_be(
            [
                "Would you like to add a long name? (this will be displayed instead of command"
            ]
        )
        .input(DESCRIPTION)
        .then_output_should_be(
            ["Would you like to add a description? (this will be displayed along side"],
            True,
        )
        .exit()
    )

    app_file = read_hexagon_config(__file__)
    created_tool = app_file["tools"][1]
    assert created_tool["action"] == "open_link"
    assert created_tool["type"] == "web"
    assert created_tool["alias"] == "olt"


def test_create_new_python_module_tool():
    (
        as_a_user(__file__)
        .given_a_cli_yaml(base_app_file)
        .run_hexagon()
        .with_shared_behavior(_shared_assertions)
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be([["Choose the action of your tool:", "new_action"]])
        .input("a-new-action")
        .then_output_should_be(
            [["What name would you like to give your new action?", "a-new-action"]]
        )
        .then_output_should_be(["What type of tool is it?", "web", "shell"])
        .carriage_return()
        .then_output_should_be([["What type of tool is it?", "shell"]])
        .input("-command")
        .then_output_should_be(
            [["What command would you like to give your tool?", "a-new-action-command"]]
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
            ]
        )
        .then_output_should_be(
            ["Would you like to add a description? (this will be displayed along side"],
            True,
        )
        .exit()
    )

    app_file = read_hexagon_config(__file__)
    created_tool = app_file["tools"][1]
    assert created_tool["action"] == "a-new-action"
    assert created_tool["type"] == "shell"
    assert created_tool["alias"] == "anac"

    assert os.path.isfile(
        os.path.join(e2e_test_folder_path(__file__), "a-new-action/__init__.py")
    )
    assert os.path.isfile(
        os.path.join(e2e_test_folder_path(__file__), "a-new-action/README.md")
    )

    shutil.rmtree(os.path.join(e2e_test_folder_path(__file__), "a-new-action"))


def test_create_tool_creates_custom_tools_dir():
    custom_tools_dir_name = "custom-tools-dir"
    app_file = base_app_file.copy()
    app_file["cli"].pop("custom_tools_dir", None)

    custom_tools_dir_path = os.path.join(
        e2e_test_folder_path(__file__), custom_tools_dir_name
    )
    if os.path.isdir(custom_tools_dir_path):
        shutil.rmtree(custom_tools_dir_path)
    os.mkdir(custom_tools_dir_path)

    (
        as_a_user(__file__)
        .given_a_cli_yaml(app_file)
        .run_hexagon()
        .with_shared_behavior(_shared_assertions)
        .arrow_down()
        .arrow_down()
        .enter()
        .input("a-new-action")
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
            True,
        )
        .input(f"/{custom_tools_dir_name}")
        .exit()
    )

    config_file = read_hexagon_config(__file__)

    assert config_file["cli"]["custom_tools_dir"] == f"./{custom_tools_dir_name}"

    assert os.path.isfile(
        os.path.join(
            e2e_test_folder_path(__file__),
            custom_tools_dir_name,
            "a-new-action/__init__.py",
        )
    )
    assert os.path.isfile(
        os.path.join(
            e2e_test_folder_path(__file__),
            custom_tools_dir_name,
            "a-new-action/README.md",
        )
    )

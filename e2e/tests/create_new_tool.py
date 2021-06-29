from e2e.tests.utils.hexagon_config import read_config_file
from e2e.tests.utils.path import e2e_test_folder_path
from e2e.tests.utils.run import run_hexagon_e2e_test, write_to_process
from e2e.tests.utils.assertions import assert_process_output, assert_process_ended
from e2e.tests.utils.cli import ARROW_DOWN_CHARACTER
import os
from ruamel.yaml import YAML
import shutil

LONG_NAME = "Custom Action Test"
DESCRIPTION = "Hexagon Custom Action Test Description"

app_file_path = os.path.join(e2e_test_folder_path(__file__), "app.yml")
base_app_file = {
    "cli": {"name": "Test", "command": "hexagon-test", "custom_tools_dir": "."},
    "tools": {"google": {"long_name": "Google", "type": "web", "action": "open_link"}},
    "envs": {},
}


def _write_app_file(app_file):
    with open(app_file_path, "w") as file:
        YAML().dump(app_file, file)


def _shared_assertions(process):
    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "Hi, which tool would you like to use today?",
            "┌──────────────────────────────────────────────────────────────────────────────",
            "",
            "",
            "",
            "⦾ Google",
            "",
            "⬡ Save Last Command as Linux Alias",
            "",
            "⬡ Create A New Tool",
            "",
            "└──────────────────────────────────────────────────────────────────────────────",
            "",
        ],
    )

    write_to_process(process, f"{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}\n")

    assert_process_output(
        process,
        [["Hi, which tool would you like to use today?", "⬡ Create A New Tool"]],
    )

    assert_process_output(
        process,
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
        ],
    )


def test_create_new_open_link_tool():
    _write_app_file(base_app_file)
    process = run_hexagon_e2e_test(__file__)
    _shared_assertions(process)

    write_to_process(process, f"{ARROW_DOWN_CHARACTER}\n")

    assert_process_output(process, [["Choose the action of your tool:", "open_link"]])

    assert_process_output(process, ["What type of tool is it?", "web", "shell"])

    write_to_process(process, "\r")
    assert_process_output(process, [["What type of tool is it?", "web"]])

    write_to_process(process, "-test\n")
    assert_process_output(
        process, [["What command would you like to give your tool?", "open-link-test"]]
    )

    write_to_process(process, "\n")
    assert_process_output(
        process, [["Would you like to add an alias/shortcut? (empty for none)", "olt"]]
    )

    write_to_process(process, f"{LONG_NAME}\n")
    assert_process_output(
        process,
        [
            "Would you like to add a long name? (this will be displayed instead of command"
        ],
    )

    write_to_process(process, f"{DESCRIPTION}\n")
    assert_process_output(
        process,
        ["Would you like to add a description? (this will be displayed along side"],
        True,
    )

    assert_process_output(
        process,
        [
            "╰╼",
            "Para repetir este comando:",
            "    hexagon-test create-tool",
        ],
        True,
    )

    assert_process_ended(process)

    app_file = read_config_file(__file__)
    created_tool = app_file["tools"]["open-link-test"]
    assert created_tool["action"] == "open_link"
    assert created_tool["type"] == "web"
    assert created_tool["alias"] == "olt"


def test_create_new_python_module_tool():
    _write_app_file(base_app_file)
    process = run_hexagon_e2e_test(__file__)
    _shared_assertions(process)

    write_to_process(process, f"{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}\n")

    assert_process_output(process, [["Choose the action of your tool:", "new_action"]])

    write_to_process(process, "a-new-action\n")

    assert_process_output(
        process, [["What name would you like to give your new action?", "a-new-action"]]
    )

    assert_process_output(process, ["What type of tool is it?", "web", "shell"])

    write_to_process(process, "\r")
    write_to_process(process, "-command\n")
    write_to_process(process, "\n")
    write_to_process(process, f"{LONG_NAME}\n")
    write_to_process(process, f"{DESCRIPTION}\n")

    assert_process_output(process, [["What type of tool is it?", "shell"]])

    assert_process_output(
        process,
        [["What command would you like to give your tool?", "a-new-action-command"]],
    )
    assert_process_output(
        process, [["Would you like to add an alias/shortcut? (empty for none)", "anac"]]
    )
    assert_process_output(
        process,
        [
            "Would you like to add a long name? (this will be displayed instead of command"
        ],
    )
    assert_process_output(
        process,
        ["Would you like to add a description? (this will be displayed along side"],
        True,
    )
    assert_process_output(
        process,
        [
            "╰╼",
            "Para repetir este comando:",
            "    hexagon-test create-tool",
        ],
        True,
    )

    assert_process_ended(process)

    app_file = read_config_file(__file__)
    created_tool = app_file["tools"]["a-new-action-command"]
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

    _write_app_file(app_file)
    process = run_hexagon_e2e_test(__file__)
    _shared_assertions(process)

    write_to_process(process, f"{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}\n")
    write_to_process(process, "a-new-action\n")
    write_to_process(process, "\r")
    write_to_process(process, "-command\n")
    write_to_process(process, "\n")
    write_to_process(process, f"{LONG_NAME}\n")
    write_to_process(process, f"{DESCRIPTION}\n")

    assert_process_output(
        process, ["│ Your CLI does not have a custom tools dir."], True
    )

    assert_process_output(
        process,
        [
            "Where would you like it to be? (can be absolute path or relative to YAML",
            "",
        ],
    )

    write_to_process(process, f"/{custom_tools_dir_name}\n")

    assert_process_ended(process)

    config_file = read_config_file(__file__)

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

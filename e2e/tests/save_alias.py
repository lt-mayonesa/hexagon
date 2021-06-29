from e2e.tests.utils.cli import ARROW_DOWN_CHARACTER
from e2e.tests.utils.assertions import assert_process_ended, assert_process_output
from e2e.tests.utils.run import discard_output, run_hexagon_e2e_test, write_to_process
import os

test_folder_path = os.path.realpath(
    os.path.join(__file__, os.path.pardir, os.path.pardir, "save_alias")
)

aliases_file_path = os.path.join(test_folder_path, "home-aliases.txt")
last_command_file_path = os.path.join(test_folder_path, "last_command")


def test_save_alias():
    with open(aliases_file_path, "w") as file:
        file.write("previous line\n")

    with open(last_command_file_path, "w") as file:
        file.write("echo works")

    process = run_hexagon_e2e_test(__file__)
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
        ],
    )
    discard_output(process, 5)
    write_to_process(process, f"{ARROW_DOWN_CHARACTER}\n")
    assert_process_output(
        process,
        [
            [
                "Hi, which tool would you like to use today?",
                "⬡ Save Last Command as Linux",
            ]
        ],
    )
    discard_output(process, 2)
    write_to_process(process, "hexagon-save-alias-test\n")
    assert_process_output(
        process,
        [
            "Ultimo comando: echo works ¿Qué alias querés crear?",
            "",
            "│ Added alias to home-aliases.txt",
            "┆",
            "",
            "",
            "# added by hexagon",
            'alias hexagon-save-alias-test="echo works"',
            "",
            "┆",
            "│",
            "╰╼",
            "Para repetir este comando:",
            "    hexagon-test save-alias",
        ],
    )

    assert_process_ended(process)

    with open(aliases_file_path, "r") as file:
        assert (
            file.read()
            == 'previous line\n\n# added by hexagon\nalias hexagon-save-alias-test="echo works"'
        )  # noqa: E501

    with open(last_command_file_path, "r") as file:
        assert file.read() == "hexagon-test save-alias"

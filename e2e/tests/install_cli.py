from e2e.tests.utils.path import e2e_test_folder_path
from e2e.tests.utils.assertions import assert_process_ended, assert_process_output
from e2e.tests.utils.run import discard_output, run_hexagon_e2e_test, write_to_process
import os

aliases_file_path = os.path.realpath(
    os.path.join(
        __file__, os.path.pardir, os.path.pardir, "install_cli", "home-aliases.txt"
    )
)


def test_install_cli():
    with open(aliases_file_path, "w") as file:
        file.write("previous line\n")

    process = run_hexagon_e2e_test(__file__, env={})
    assert_process_output(
        process,
        [
            "╭╼ Hexagon",
            "│",
            "│ This looks like your first time running Hexagon.",
            '│ You should probably run "Install CLI".',
            "│",
            "Hi, which tool would you like to use today?",
            "┌──────────────────────────────────────────────────────────────────────────────",
            "",
            "❯",
            "",
            "Install CLI                                               Install a custom",
            "",
            "└──────────────────────────────────────────────────────────────────────────────",
            "",
        ],
    )
    write_to_process(process, "\n")
    assert_process_output(
        process,
        [
            ["Hi, which tool would you like to use today?", "Install CLI"],
            "",
            "",
            "Where is your project's hexagon config file?",
            "",
            "install_cli",
        ],
    )
    discard_output(process, 5)
    write_to_process(process, "/config.yml\n")
    assert_process_output(
        process,
        [
            "│ Added alias to home-aliases.txt",
            "┆",
            "",
            "",
            "# added by hexagon",
            'alias hexagon-test="HEXAGON_CONFIG_FILE=',
            "",
            "",
            "┆",
            "│",
            "╰╼",
        ],
        discard_until_initial=True,
    )

    assert_process_ended(process)

    with open(aliases_file_path, "r") as file:
        assert (
            file.read()
            == f'previous line\n\n# added by hexagon\nalias hexagon-test="HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config.yml")} hexagon"'
        )  # noqa: E501

from e2e.tests.utils.hexagon_spec import as_a_user
import os

test_folder_path = os.path.realpath(
    os.path.join(__file__, os.path.pardir, os.path.pardir, "save_alias")
)

aliases_file_path = os.path.join(test_folder_path, "home-aliases.txt")
last_command_file_path = os.path.join(test_folder_path, "last_command")


def test_save_alias():
    with open(aliases_file_path, "w") as file:
        file.write("previous line\n")

    (as_a_user(__file__).run_hexagon().enter().exit())

    (
        as_a_user(__file__)
        .run_hexagon()
        .arrow_down()
        .enter()
        .input("hexagon-save-alias-test")
        .then_output_should_be(
            [
                "Last command: hexagon-test python-module Alias name?",
                "# added by hexagon",
                'alias hexagon-save-alias-test="hexagon-test python-module"',
                "$ hexagon-save-alias-test",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

    with open(aliases_file_path, "r") as file:
        assert (
            file.read()
            == 'previous line\n\n# added by hexagon\nalias hexagon-save-alias-test="hexagon-test python-module"'
        )

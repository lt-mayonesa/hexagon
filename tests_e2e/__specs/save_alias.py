import os
import tempfile

from tests_e2e.__specs.utils.hexagon_spec import as_a_user


def test_save_alias():
    test_folder_path = tempfile.mkdtemp(suffix="_hexagon")
    aliases_file_path = os.path.join(test_folder_path, "home-aliases.txt")
    # last_command_file_path = os.path.join(test_folder_path, "last_command")

    with open(aliases_file_path, "w") as file:
        file.write("previous line\n")

    spec = as_a_user(__file__).run_hexagon(test_dir=test_folder_path).enter().exit()

    (
        as_a_user(__file__)
        .run_hexagon(test_dir=spec.test_dir)
        .arrow_down()
        .enter()
        .input("hexagon-save-alias-test")
        .then_output_should_be(
            [
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

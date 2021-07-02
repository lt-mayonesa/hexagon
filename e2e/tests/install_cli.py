from e2e.tests.utils.path import e2e_test_folder_path
from e2e.tests.utils.hexagon_spec import as_a_user
import os

aliases_file_path = os.path.realpath(
    os.path.join(
        __file__, os.path.pardir, os.path.pardir, "install_cli", "home-aliases.txt"
    )
)


def test_install_cli():
    with open(aliases_file_path, "w") as file:
        file.write("previous line\n")

    (
        as_a_user(__file__)
        .run_hexagon(env={})
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "┌──────────────────────────────────────────────────────────────────────────────",
                "",
                "❯",
                "",
                "Install CLI                                               Install a custom",
                "",
                "└──────────────────────────────────────────────────────────────────────────────",
                "",
            ]
        )
        .enter()
        .write("/config.yml\n")
        .then_output_should_be(
            ["# added by hexagon", 'alias hexagon-test="HEXAGON_CONFIG_FILE='],
            True,
        )
        .exit()
    )

    with open(aliases_file_path, "r") as file:
        assert (
            file.read()
            == f'previous line\n\n# added by hexagon\nalias hexagon-test="HEXAGON_CONFIG_FILE={os.path.join(e2e_test_folder_path(__file__), "config.yml")} hexagon"'
        )  # noqa: E501

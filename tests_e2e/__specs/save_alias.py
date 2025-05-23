import os

from tests_e2e.framework.hexagon_spec import as_a_user


def _alias_file_path(spec):
    return os.path.join(spec.test_dir, "home-aliases.txt")


def _write_alias_file(spec):
    with open(_alias_file_path(spec), "w") as file:
        file.write("previous line\n")


def test_save_alias():
    spec = (
        as_a_user(__file__)
        .executing_first(_write_alias_file)
        .run_hexagon()
        .enter()
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon()
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

    with open(_alias_file_path(spec), "r") as file:
        assert (
            file.read()
            == 'previous line\n\n# added by hexagon\nalias hexagon-save-alias-test="hexagon-test python-module"'
        )

import pytest

from tests_e2e.framework.hexagon_spec import as_a_user

# this updates automatically https://python-semantic-release.readthedocs.io/en/latest/index.html
__version__ = "0.63.1"


@pytest.mark.parametrize("command", ["--version", "-v"])
def test_print_hexagon_installed_version(command):
    (
        as_a_user(__file__)
        .run_hexagon([command], os_env_vars={"HEXAGON_THEME": "disabled"})
        .then_output_should_be(
            [
                f"Hexagon: {__version__}",
            ],
            ignore_blank_lines=False,
        )
        .exit()
    )

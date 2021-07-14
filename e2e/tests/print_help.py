import pytest

from e2e.tests.utils.hexagon_spec import as_a_user


@pytest.mark.parametrize("command", ["--help", "-h"])
def test_print_help_using_yaml_contents(command):
    (
        as_a_user(__file__)
        .run_hexagon([command], os_env_vars={"HEXAGON_THEME": "disabled"})
        .then_output_should_be(
            [
                "Test",
                "",
                "Envs:",
                " dev (d)                                                     Development",
                "                                                             this env has a",
                "description",
                "",
                " qa (q)                                                      Quality Assurance",
                "",
                "",
                "Tools:",
                "",
                "web:",
                "  google                                                      Google",
                "",
                "shell:",
                "  python-module (pm)                                          Python Module Test",
                "                                                            This is a",
                "description that should be rendered",
                "",
                "  python-module-env (pme)                                     Python Module Env",
                "Test",
                "",
                "hexagon:",
                "  save-alias                                                  Save Last Command",
                "as Linux Alias",
                "  create-tool                                                 Create A New Tool",
            ]
        )
        .exit()
    )


@pytest.mark.parametrize("command", ["--help", "-h"])
def test_print_help_using_yaml_contents_no_tools(command):
    (
        as_a_user(__file__)
        .given_a_cli_yaml(
            {
                "cli": {
                    "name": "Test",
                    "command": "hexagon-test",
                    "custom_tools_dir": ".",
                },
                "tools": [],
                "envs": [],
            }
        )
        .run_hexagon([command], os_env_vars={"HEXAGON_THEME": "disabled"})
        .then_output_should_be(
            [
                "Test",
                "",
                "Envs:",
                "",
                "Tools:",
                "",
            ]
        )
        .exit()
    )

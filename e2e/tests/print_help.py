import pytest

from e2e.tests.utils.hexagon_spec import as_a_user


@pytest.mark.parametrize("command", ["--help", "-h"])
def test_print_help_using_yaml_contents(command):
    (
        as_a_user(__file__)
        .given_a_cli_yaml(
            {
                "cli": {
                    "name": "Test",
                    "command": "hexagon-test",
                    "custom_tools_dir": ".",
                },
                "tools": [
                    {
                        "name": "google",
                        "long_name": "Google",
                        "type": "web",
                        "action": "open_link",
                        "envs": {"*": "https://www.google.com/"},
                    },
                    {
                        "name": "python-module",
                        "action": "python-module",
                        "type": "shell",
                        "alias": "pm",
                        "long_name": "Python Module Test",
                        "description": "This is a description that should be rendered",
                    },
                    {
                        "name": "python-module-env",
                        "action": "python-module",
                        "type": "shell",
                        "alias": "pme",
                        "long_name": "Python Module Env Test",
                        "envs": {
                            "dev": [789, "ghi"],
                            "qa": {"foo": "foo", "bar": "bar"},
                        },
                    },
                ],
                "envs": [
                    {
                        "name": "dev",
                        "alias": "d",
                        "long_name": "Development",
                        "description": "this env has a description",
                    },
                    {"name": "qa", "alias": "q", "long_name": "Quality Assurance"},
                ],
            }
        )
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
                "as Shell Alias",
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
        .then_output_should_be(["Test", "", "Envs:", "", "", "Tools:", "", ""])
        .exit()
    )

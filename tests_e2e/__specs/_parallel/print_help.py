import pytest

from tests_e2e.framework.hexagon_spec import as_a_user


@pytest.mark.parametrize("command", ["--help", "-h"])
def test_print_help_using_yaml_contents(command):
    (
        as_a_user(__file__)
        .given_a_cli_yaml(
            {
                "cli": {
                    "name": "Test CLI",
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
                        "description": "This is",
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
                    {"name": "dev", "alias": "d", "long_name": "Development"},
                    {
                        "name": "qa",
                        "alias": "q",
                        "long_name": "Quality Assurance",
                        "description": "QA Environment",
                    },
                ],
            }
        )
        .run_hexagon([command], os_env_vars={"HEXAGON_THEME": "disabled"})
        .then_output_should_be(
            [
                "Test CLI",
                "",
                "usage: hexagon-test [tool] [env] [[positional-tool-arg] [--optional-tool-arg=123] ...]",
                "",
                "Envs:",
                " dev (d)                                                     Development",
                "",
                " qa (q)                                                      Quality Assurance",
                "                                                             QA Environment",
                "",
                "Tools:",
                "",
                "web:",
                "  google                                                      Google",
                "",
                "shell:",
                "  python-module (pm)                                          Python Module Test",
                "                                                              This is a description that should be rendered",  # noqa
                "",
                "  python-module-env (pme)                                     Python Module Env Test",
                "                                                              This is",
                "",
                "hexagon:",
                "  save-alias                                                  Save Last Command as Shell Alias",
                "  replay (r)                                                  Replay Last Command",
                "  create-tool                                                 Create A New Tool",
            ],
            ignore_blank_lines=False,
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
                    "name": "Test CLI",
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
                "Test CLI",
                "",
                "usage: hexagon-test [tool] [env] [[positional-tool-arg] [--optional-tool-arg=123] ...]",
                "",
                "Envs:",
                "",
                "Tools:",
                "",
                "",
            ],
            ignore_blank_lines=False,
        )
        .exit()
    )

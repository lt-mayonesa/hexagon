from e2e.tests.utils.hexagon_spec import as_a_user


def test_show_errors_when_invalid_yaml():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "There was an error validating your YAML",
                "3 validation errors for ConfigFile",
                "cli -> command",
                "field required (type=value_error.missing)",
                "envs",
                "field required (type=value_error.missing)",
                "tools -> 0 -> action",
                "field required (type=value_error.missing)",
            ]
        )
        .exit(status=1)
    )

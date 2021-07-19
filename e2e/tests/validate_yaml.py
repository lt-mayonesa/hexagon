from e2e.tests.utils.hexagon_spec import as_a_user


def test_show_errors_when_invalid_yaml():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "There were 4 error(s) in your YAML",
                "",
                "cli.command -> str type expected",
                "2   name: Test",
                "3   custom_tools_dir: .",
                "4   command: [ 'test' ]",
                "5",
                "6 tools:",
                "",
                "" "envs -> field required",
                "",
                "",
                "tools.1.action -> field required",
                "13",
                "14",
                "15   - name: google-invalid",
                "16     long_name: Google",
                "17     type: web",
                "",
                "tools.2.action -> none is not an allowed value",
                "19   - name: another-invalid",
                "20     long_name: Google 2",
                "21     type: web",
                "22     action:",
            ]
        )
        .exit(status=1)
    )

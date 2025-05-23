from tests_e2e.framework.hexagon_spec import as_a_user


def test_show_errors_when_invalid_yaml():
    (
        as_a_user(__file__)
        .run_hexagon()
        .then_output_should_be(
            [
                "There were 7 error(s) in your YAML file:",
                "",
                "✗ cli.command -> Input should be a valid string",
                "2   name: Test",
                "3   custom_tools_dir: .",
                "4   command: [ 'test' ]",
                "5",
                "6 tools",
                "",
                "✗ envs -> Field required",
                "1",
                "",
                "✗ tools.1.action -> Field required",
                "13       '*': https://www.google.com/",
                "14",
                "15   - name: google-invalid",
                "16     long_name: Google",
                "17     type: web",
                "",
                "✗ tools.1.tools -> Field required",
                "13       '*': https://www.google.com/",
                "14",
                "15   - name: google-invalid",
                "16     long_name: Google",
                "17     type: web",
                "",
                "✗ tools.2.action.str -> Input should be a valid string",
            ],
            ignore_blank_lines=False,
        )
        .exit(status=1)
    )

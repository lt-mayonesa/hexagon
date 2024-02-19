import pytest

from hexagon.actions.internal.replay import __command_str_to_list


@pytest.mark.parametrize(
    "command,expected",
    [
        ("hexagon-test", ["hexagon-test"]),
        ("1", ["1"]),
        ("hexagon-test python-module", ["hexagon-test", "python-module"]),
        ('"only one spaced arg"', ["only one spaced arg"]),
        ("'only one spaced arg'", ["only one spaced arg"]),
        ("--key=value", ["--key=value"]),
        ("--key='value'", ["--key=value"]),
        ('--key="value"', ["--key=value"]),
        ('-k="value"', ["-k=value"]),
        ("-k value", ["-k", "value"]),
        (
            "'only one spaced arg' \"another spaced arg\"",
            ["only one spaced arg", "another spaced arg"],
        ),
        ('--key="My father\'s name"', ["--key=My father's name"]),
        ("-f 'the play \"otelo\" had started'", ["-f", 'the play "otelo" had started']),
        (
            "hexagon-test python-module john 10",
            ["hexagon-test", "python-module", "john", "10"],
        ),
        (
            'hexagon-test python-module john 10 --country="The Netherlands" --likes=orange',
            [
                "hexagon-test",
                "python-module",
                "john",
                "10",
                "--country=The Netherlands",
                "--likes=orange",
            ],
        ),
        (
            "hexagon-test python-module john 10 --country='The Netherlands' --likes=orange",
            [
                "hexagon-test",
                "python-module",
                "john",
                "10",
                "--country=The Netherlands",
                "--likes=orange",
            ],
        ),
    ],
)
def test_string_is_converted_to_expected_list(command, expected):
    assert __command_str_to_list(command) == expected

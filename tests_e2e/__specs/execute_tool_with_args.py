import sys

import pytest

from tests_e2e.__specs.utils.assertions import assert_file_has_contents
from tests_e2e.__specs.utils.hexagon_spec import as_a_user


def test_execute_python_tool_with_one_positional_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(["p-m-args", "John"])
        .then_output_should_be(
            [
                "name: John",
                "age: None",
                "nationality: Argentinian",
                "car_brand: Ford",
                "car_model: None",
                "car_years: None",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test p-m-args John",
    )


def test_execute_python_tool_with_several_positional_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(["p-m-args", "John", "31", "French"])
        .then_output_should_be(
            [
                "name: John",
                "age: 31",
                "nationality: French",
                "car_brand: Ford",
                "car_model: None",
                "car_years: None",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test p-m-args John 31 French",
    )


@pytest.mark.parametrize(
    "args",
    [
        ["--name=John", "--age", "31", "--country", "Argentina", "--likes", "sand", "beach"],  # fmt: skip
        ["--likes", "sand", "beach", "--name=John", "--country", "Argentina", "--age", "31"],  # fmt: skip
        ["--name=John", "--age", "31", "--country", "Argentina", "--likes", "sand", "beach"],  # fmt: skip
        ["-n=John", "-a", "31", "-c", "Argentina", "-l", "sand", "beach"],  # fmt: skip
    ],
)
def test_only_optional_arguments(args):
    (
        as_a_user(__file__)
        .run_hexagon(["only-optionals"] + args)
        .then_output_should_be(
            [
                "name: John",
                "age: 31",
                "country: Argentina",
                "likes: ['sand', 'beach']",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test only-optionals --name=John --age=31 --country=Argentina --likes=sand --likes=beach",
    )


def test_arguments_type_matters():
    (
        as_a_user(__file__)
        .run_hexagon(["p-m-args", "John", "not-a-number"])
        .exit(status=1)
    )


def test_optional_arguments_as_list():
    (
        as_a_user(__file__)
        .run_hexagon(["p-m-args", "John", "--car-years", "1997", "1998"])
        .then_output_should_be(
            [
                "name: John",
                "age: None",
                "nationality: Argentinian",
                "car_brand: Ford",
                "car_model: None",
                "car_years: ['1997', '1998']",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test p-m-args John --car-years=1997 --car-years=1998",
    )


@pytest.mark.parametrize(
    "help_arg",
    [
        "--help",
        "-h",
    ],
)
def test_show_tool_help_text_when_tool_has_args(help_arg):
    (
        as_a_user(__file__)
        .run_hexagon(["p-m-args", help_arg])
        .then_output_should_be(
            [
                (
                    "usage: p-m-args [-h] [--car-brand [CAR_BRAND]] [--car-model [CAR_MODEL]] [--car-years [CAR_YEARS ...]] [name] [age] [nationality]"
                    if sys.version_info >= (3, 9)
                    else "usage: p-m-args [-h] [--car-brand [CAR_BRAND]] [--car-model [CAR_MODEL]] [--car-years [CAR_YEARS [CAR_YEARS ...]]] [name] [age] [nationality]"
                ),
                "",
                "Python Module Script With Args",
                "",
                "positional arguments:",
                "  name                  name (default: None)",
                "  age                   the person's age, if provided must be greater than 18 (default: None)",
                "  nationality           nationality (default: Argentinian)",
                "",
                "options:" if sys.version_info >= (3, 10) else "optional arguments:",
                "  -h, --help            show this help message and exit",
                "  --car-brand [CAR_BRAND], -cb [CAR_BRAND]",
                "                        the car's brand (default: Ford)",
                "  --car-model [CAR_MODEL], -cm [CAR_MODEL]",
                "                        the car's model (default: None)",
                (
                    "  --car-years [CAR_YEARS ...], -cy [CAR_YEARS ...]"
                    if sys.version_info >= (3, 9)
                    else "  --car-years [CAR_YEARS [CAR_YEARS ...]], -cy [CAR_YEARS [CAR_YEARS ...]]"
                ),
                "                        car_years (default: None)",
                "",
                "To support tool arguments either add a model extending",
                "hexagon.domain.args.ToolArgs class to your script,",
                "or a args property in the tool YAML definition.",
            ]
        )
        .exit()
    )


@pytest.mark.parametrize(
    "help_arg",
    [
        "--help",
        "-h",
    ],
)
def test_show_tool_help_text_when_tool_has_no_args(help_arg):
    (
        as_a_user(__file__)
        .run_hexagon(["no-args", help_arg])
        .then_output_should_be(
            [
                "usage: no-args [-h]",
                "",
                "Python Module Script With No Args",
                "",
                "options:" if sys.version_info >= (3, 10) else "optional arguments:",
                ["  -h, --help", "show this help message and exit"],
                "",
                "To support tool arguments either add a model extending",
                "hexagon.domain.args.ToolArgs class to your script,",
                "or a args property in the tool YAML definition.",
            ]
        )
        .exit()
    )

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
                "nationality: None",
                "car_brand: None",
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
        .run_hexagon(["p-m-args", "John", "31", "Argentine"])
        .then_output_should_be(
            [
                "name: John",
                "age: 31",
                "nationality: Argentine",
                "car_brand: None",
                "car_model: None",
                "car_years: None",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test p-m-args John 31 Argentine",
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
                "nationality: None",
                "car_brand: None",
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

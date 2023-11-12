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


def test_should_only_trace_passed_arguments_and_not_defaults():
    (
        as_a_user(__file__)
        .run_hexagon(["p-m-args", "John", "31", "Argentinian", "--car-brand", "Ford"])
        .then_output_should_be(
            [
                "name: John",
                "age: 31",
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
        "hexagon-test p-m-args John 31 Argentinian --car-brand=Ford",
    )


def test_should_argument_should_be_traced_once():
    (
        as_a_user(__file__)
        .run_hexagon(["access-multiple-times", "John"])
        .then_output_should_be(
            [
                "name: John",
                "name: John",
                "name: John",
                "name: John",
                "name: John",
                "name: John",
            ]
        )
        .exit()
    )
    assert_file_has_contents(
        __file__,
        ".config/test/last-command.txt",
        "hexagon-test access-multiple-times John",
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
        .run_hexagon(
            ["p-m-args", "John", "not-a-number", "USA", "--car-brand", "Chevrolet"]
        )
        .then_output_should_be(
            [
                "There where 3 error(s) in your input",
                "",
                "✗ age -> value is not a valid integer",
                "",
                "✗ nationality -> USA is not a valid nationality",
                "",
                "✗ car_brand -> we don't accept Chevrolet cars",
            ],
            ignore_blank_lines=False,
        )
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
            ],
            ignore_blank_lines=False,
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
            ],
            ignore_blank_lines=False,
        )
        .exit()
    )


def test_tool_args_class_can_be_used_to_prompt():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_name_and_age"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .then_output_should_be(
            ["input the person's name:"], discard_until_first_match=True
        )
        .input("John")
        .then_output_should_be(["name: John"], discard_until_first_match=True)
        .input("24")
        .then_output_should_be(
            ["age: 24", "age type: int"], discard_until_first_match=True
        )
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_name_and_age --name=John --age=24",
                "or:",
                "hexagon-test p prompt_name_and_age -n=John -a=24",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_prompt_validates_input_correctly():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_validate_age"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .input("2")
        .erase()
        .input("3")
        .erase()
        .input("58")
        .erase()
        .input("49")
        .erase()
        .input("36")
        .then_output_should_be(["age: 36"], discard_until_first_match=True)
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_validate_age --age=36",
                "or:",
                "hexagon-test p prompt_validate_age -a=36",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_prompt_shows_default_value():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_show_default_value"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .then_output_should_be(["country: Argentina"], discard_until_first_match=True)
        .enter()
        .then_output_should_be(["country: Argentina"], discard_until_first_match=True)
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_show_default_value --country=Argentina",
                "or:",
                "hexagon-test p prompt_show_default_value -c=Argentina",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_prompt_shows_default_value_input_another():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_show_default_value"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .then_output_should_be(["country: Argentina"], discard_until_first_match=True)
        .erase("Argentina")
        .input("Colombia")
        .then_output_should_be(["country: Colombia"], discard_until_first_match=True)
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_show_default_value --country=Colombia",
                "or:",
                "hexagon-test p prompt_show_default_value -c=Colombia",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_prompt_list_value_using_multiline():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_list_value"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .then_output_should_be(
            ["likes: (each line represents a value) ESC + Enter to finish input"],
            discard_until_first_match=True,
        )
        .input("pizza")
        .input("pasta")
        .input("sushi")
        .esc()
        .carriage_return()
        .then_output_should_be(
            ["likes: ['pizza', 'pasta', 'sushi']"], discard_until_first_match=True
        )
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_list_value --likes=pizza --likes=pasta --likes=sushi",
                "or:",
                "hexagon-test p prompt_list_value -l=pizza -l=pasta -l=sushi",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_prompt_support_enum_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_enum_choices"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .then_output_should_be(
            ["tag", "A", "B", "C", "D", "E", "F"], discard_until_first_match=True
        )
        .arrow_up()  # default is C
        .carriage_return()
        .then_output_should_be(
            ["tag: b", "tag type: Category"], discard_until_first_match=True
        )
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_enum_choices --tag=b",
                "or:",
                "hexagon-test p prompt_enum_choices -t=b",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_prompt_support_list_of_enum_arguments():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_list_enum_choices"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .then_output_should_be(
            ["available_tags", "A", "◉ B", "C", "D", "◉ E", "F"],
            discard_until_first_match=True,
        )
        .space_bar()
        .arrow_down()
        .arrow_down()
        .arrow_down()
        .space_bar()
        .arrow_down()
        .space_bar()
        .arrow_down()
        .space_bar()
        .carriage_return()
        .then_output_should_be(
            [
                "available_tags: [<Category.A: 'a'>, <Category.B: 'b'>, <Category.D: 'd'>, <Category.F: 'f'>]"
            ],
            discard_until_first_match=True,
        )
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_list_enum_choices --available-tags=a --available-tags=b --available-tags=d --available-tags=f",  # noqa: E501
                "or:",
                "hexagon-test p prompt_list_enum_choices -at=a -at=b -at=d -at=f",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_should_validate_type():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_validate_type"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .write("23")
        .write(".")
        .write("5")
        .enter()
        .then_output_should_be(["total_amount: 23.05"], discard_until_first_match=True)
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_validate_type --total-amount=23.05",
                "or:",
                "hexagon-test p prompt_validate_type -ta=23.05",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_should_prompt_same_arg_multiple_times_successfully():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_multiple_times"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .input("John")
        .then_output_should_be(["name: John"], discard_until_first_match=True)
        .input("Richard")
        .then_output_should_be(["name: Richard"], discard_until_first_match=True)
        .input("Jose")
        .then_output_should_be(["name: Jose"], discard_until_first_match=True)
        .input("Carlos")
        .then_output_should_be(["name: Carlos"], discard_until_first_match=True)
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_multiple_times --name=Carlos",
                "or:",
                "hexagon-test p prompt_multiple_times -n=Carlos",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_should_prompt_same_positional_arg_multiple_times_successfully():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .input("one")
        .then_output_should_be(["test: one"], discard_until_first_match=True)
        .input("two")
        .then_output_should_be(["test: two"], discard_until_first_match=True)
        .input("three")
        .then_output_should_be(["test: three"], discard_until_first_match=True)
        .input("four")
        .then_output_should_be(["test: four"], discard_until_first_match=True)
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt four",
                "or:",
                "hexagon-test p four",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_should_prompt_fuzzy_search():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_fuzzy_search"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .input("astm")
        .then_output_should_be(
            ["fuzzy_input: a sentence to match"], discard_until_first_match=True
        )
        .input("astm")
        .then_output_should_be(
            ["fuzzy_input: another sentence to match"], discard_until_first_match=True
        )
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test prompt prompt_fuzzy_search --fuzzy-input=another sentence to match",
                "or:",
                "hexagon-test p prompt_fuzzy_search -fi=another sentence to match",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_should_prompt_fuzzy_file_search():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_fuzzy_file"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .then_output_should_be(
            [
                "",
                "",
                "Enter fuzzy_file_input",
                "4/4",
                "01_file.txt",
                "02_file.txt",
                "03_file.txt",
            ],
        )
        .input("file_c")
        .exit()
    )


def test_should_prompt_fuzzy_file_search_with_generic_choice():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_fuzzy_file_generic"],
            os_env_vars={"HEXAGON_THEME": "no_border"},
        )
        .then_output_should_be(
            [
                "",
                "",
                "Enter fuzzy_file_input",
                "5/5",
                "Any",
                "01_file.txt",
                "02_file.txt",
                "03_file.txt",
            ],
        )
        .carriage_return()
        .then_output_should_be(
            ["fuzzy_file_input_generic: ::generic::"], discard_until_first_match=True
        )
        .exit()
    )


def test_should_prompt_yes_no_confirmation():
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_boolean"],
        )
        .then_output_should_be(
            ["Do you want to continue? (Y/n)"],
        )
        .write("y")
        .then_output_should_be(
            [
                "Do you want to continue? Yes",
                "proceed: True",
            ],
        )
        .exit()
    )
    (
        as_a_user(__file__)
        .run_hexagon(
            ["prompt", "prompt_boolean"],
        )
        .then_output_should_be(
            ["Do you want to continue? (Y/n)"],
        )
        .write("n")
        .then_output_should_be(
            [
                "Do you want to continue? No",
                "proceed: False",
            ],
        )
        .exit()
    )


def test_should_handle_prompt_on_access_true():
    (
        as_a_user(__file__)
        .run_hexagon(["prompt-on-access"])
        .then_output_should_be(
            [
                "Enter name:",
            ]
        )
        .input("John")
        .then_output_should_be(
            [
                "Enter name: John",
                "name: John",
            ],
        )
        .then_output_should_be(
            [
                "Enter age:",
            ]
        )
        .input("24")
        .then_output_should_be(
            [
                "Enter age: 24",
                "age: 24",
            ]
        )
        .then_output_should_be(
            [
                "Enter age:",
            ]
        )
        .input("45")
        .then_output_should_be(
            [
                "Enter age: 45",
                "age 2: 45",
            ]
        )
        .exit()
    )

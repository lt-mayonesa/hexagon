import pytest
from InquirerPy import inquirer

from hexagon.cli.wax import search_by_key_or_alias, select_tool, select_env


def inquirer_mock(ret):
    class FuzzyMock:
        @staticmethod
        def execute():
            return ret

    class TestArgs(object):
        def __call__(
            self, message: str, choices: list, validate: object, invalid_message: str
        ):
            self.args = list([message, choices, validate, invalid_message])
            return FuzzyMock()

    return TestArgs()


@pytest.fixture
def tool_mock():
    return inquirer_mock("docker")


@pytest.fixture
def env_mock():
    return inquirer_mock("dev")


tools_dict = {"docker": {"alias": "d"}, "bastion": {"alias": "b"}, "no_alias": {}}

envs_dict = {"dev": {"alias": "d"}, "qa": {"alias": "q"}}


@pytest.mark.parametrize(
    "search,expected",
    [
        (None, None),
        ("", None),
        ("docker", "docker"),
        ("d", "docker"),
        ("b", "bastion"),
        ("no_alias", "no_alias"),
        ("unknown_tool", None),
    ],
)
def test_search_tools_dict_by_key_or_alias(search, expected):
    assert search_by_key_or_alias(tools_dict, search) == expected


def test_tool_is_selected_from_cmd():
    assert select_tool(tools_dict, "docker") == ("docker", {"alias": "d"})


def test_tool_is_selected_by_prompt(monkeypatch, tool_mock):
    monkeypatch.setattr(inquirer, "fuzzy", tool_mock)

    assert select_tool(tools_dict) == ("docker", {"alias": "d"})
    assert tool_mock.args[0] == "Hi, which tool would you like to use today?"
    assert tool_mock.args[1] == [
        {"value": "docker", "name": "  docker"},
        {"value": "bastion", "name": "  bastion"},
        {"value": "no_alias", "name": "  no_alias"},
    ]
    assert tool_mock.args[3] == "Please select a valid tool"


def test_tool_has_no_env_property():
    assert select_env(envs_dict, None) == (None, None)


def test_tool_has_env_property_with_wildcard():
    assert select_env(envs_dict, {"*": "sarasa"}) == (None, "sarasa")


def test_env_is_selected_from_cmd():
    tool_envs = {"dev": "env_1", "qa": "env_2"}
    assert select_env(envs_dict, tool_envs, "qa") == ("qa", "env_2")


def test_env_is_selected_by_prompt(monkeypatch, env_mock):
    tool_envs = {"dev": "env_1", "qa": "env_2"}
    monkeypatch.setattr(inquirer, "fuzzy", env_mock)

    assert select_env(envs_dict, tool_envs) == ("dev", "env_1")
    assert env_mock.args[0] == "On which environment?"
    assert env_mock.args[1] == [
        {"value": "dev", "name": "dev"},
        {"value": "qa", "name": "qa"},
    ]
    assert env_mock.args[3] == "Please select a valid environment"

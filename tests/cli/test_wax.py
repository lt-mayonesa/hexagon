import pytest
from InquirerPy import inquirer

from hexagon.domain.tool import Tool
from hexagon.domain.env import Env
from hexagon.support.analytics import UserEvent
from hexagon.support.wax import search_by_name_or_alias, select_tool, select_env
from hexagon.support import analytics


def args_mock(ret):
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
    return args_mock("docker")


@pytest.fixture
def env_mock():
    return args_mock("dev")


@pytest.fixture
def analytics_mock():
    class TestArgs(object):
        def __call__(self, e: UserEvent, **kwargs):
            self.args = {"e": e, **kwargs}
            return

    return TestArgs()


tools = [
    Tool(name="docker", alias="d", action="docker_run"),
    Tool(name="bastion", alias="b", action="bastion"),
    Tool(name="no_alias", action="some_action"),
]

envs = [Env(name="dev", alias="d"), Env(name="qa", alias="q")]


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
    assert search_by_name_or_alias(tools, search) == expected


def test_tool_is_selected_from_cmd(monkeypatch, analytics_mock):
    monkeypatch.setattr(analytics, "user_event", analytics_mock)

    assert select_tool(tools, "docker") == Tool(
        name="docker", alias="d", action="docker_run"
    )


def test_tool_is_selected_by_prompt(monkeypatch, tool_mock, analytics_mock):
    monkeypatch.setattr(inquirer, "fuzzy", tool_mock)
    monkeypatch.setattr(analytics, "user_event", analytics_mock)

    assert select_tool(tools) == Tool(name="docker", alias="d", action="docker_run")
    assert tool_mock.args[0] == "action.support.wax.select_tool"
    assert tool_mock.args[1] == [
        {"value": "docker", "name": "  docker"},
        {"value": "bastion", "name": "  bastion"},
        {"value": "no_alias", "name": "  no_alias"},
    ]
    assert tool_mock.args[3] == "error.support.wax.invalid_tool"


def test_tool_has_no_env_property():
    assert select_env(envs, None) == (None, None)


def test_tool_has_env_property_with_wildcard():
    assert select_env(envs, {"*": "sarasa"}) == (None, "sarasa")


def test_env_is_selected_from_cmd(monkeypatch, analytics_mock):
    monkeypatch.setattr(analytics, "user_event", analytics_mock)

    tool_envs = {"dev": "env_1", "qa": "env_2"}
    assert select_env(envs, tool_envs, "qa") == (envs[1], "env_2")


def test_env_is_selected_by_prompt(monkeypatch, env_mock, analytics_mock):
    tool_envs = {"dev": "env_1", "qa": "env_2"}
    monkeypatch.setattr(inquirer, "fuzzy", env_mock)
    monkeypatch.setattr(analytics, "user_event", analytics_mock)

    assert select_env(envs, tool_envs) == (envs[0], "env_1")
    assert env_mock.args[0] == "action.support.wax.select_environment"
    assert env_mock.args[1] == [
        {"value": "dev", "name": "dev"},
        {"value": "qa", "name": "qa"},
    ]
    assert env_mock.args[3] == "error.support.wax.invalid_environment"

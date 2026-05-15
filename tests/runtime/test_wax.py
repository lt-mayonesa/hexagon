import pytest

from hexagon.domain.env import Env
from hexagon.domain.tool import Tool
from hexagon.runtime import wax


@pytest.fixture(autouse=True)
def mock_i18n(monkeypatch):
    monkeypatch.setattr(wax, "_", value=lambda x: x, raising=False)
    yield


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
def test_search_by_name_or_alias_returns_correct_tool_name(search, expected):
    """
    Given a list of tools with names and aliases.
    When searching for a tool by its name or alias.
    Then the tool's name should be returned if found, otherwise None.
    """
    assert wax.search_by_name_or_alias(tools, search) == expected

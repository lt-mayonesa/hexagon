import pytest

from hexagon.domain.env import Env
from hexagon.domain.tool import Tool
from hexagon.runtime import wax
from hexagon.support.input.prompt import prompt


def args_mock(ret):
    class TestArgs(object):
        def __call__(
            self, message: str, choices: list, validate: object, invalid_message: str
        ):
            self.args = list([message, choices, validate, invalid_message])
            return ret

    return TestArgs()


@pytest.fixture(autouse=True)
def mock_i18n(monkeypatch):
    monkeypatch.setattr(wax, "_", value=lambda x: x, raising=False)
    yield


@pytest.fixture
def tool_mock():
    return args_mock("docker")


@pytest.fixture
def env_mock():
    return args_mock("dev")


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


def test_select_tool_returns_correct_tool_when_specified_in_command(monkeypatch):
    """
    Given a list of tools with names and aliases.
    When selecting a tool by the name 'docker' from command line.
    Then the Tool object with name='docker', alias='d', action='docker_run' should be returned.
    """
    assert wax.select_tool(tools, "docker") == Tool(
        name="docker", alias="d", action="docker_run"
    )


def test_select_tool_prompts_user_when_no_tool_specified(monkeypatch, tool_mock):
    """
    Given a list of tools with names and aliases.
    When no tool is specified in command line.
    Then user should be prompted to select a tool with a fuzzy search interface.
    And the Tool object matching the user's selection ('docker') should be returned.
    """
    monkeypatch.setattr(prompt, "fuzzy", tool_mock)

    assert wax.select_tool(tools) == Tool(name="docker", alias="d", action="docker_run")
    assert tool_mock.args[0] == "action.support.wax.select_tool"
    assert tool_mock.args[1] == [
        {"value": "docker", "name": "  docker"},
        {"value": "bastion", "name": "  bastion"},
        {"value": "no_alias", "name": "  no_alias"},
    ]
    assert tool_mock.args[3] == "error.support.wax.invalid_tool"


def test_select_env_returns_none_when_tool_has_no_env_property():
    """
    Given a tool with env property set to None.
    When calling select_env with this tool's env property.
    Then a tuple of (None, None) should be returned for both env and env_args.
    """
    assert wax.select_env(envs, None) == (None, None)


def test_select_env_returns_wildcard_value_when_tool_has_wildcard_env_property():
    """
    Given a tool with env property containing a wildcard key '*' with value 'sarasa'.
    When calling select_env with this tool's env property.
    Then a tuple of (None, 'sarasa') should be returned for env and env_args.
    """
    assert wax.select_env(envs, {"*": "sarasa"}) == (None, "sarasa")


def test_select_env_returns_correct_env_when_specified_in_command(monkeypatch):
    """
    Given a list of environments and a tool_envs dictionary mapping 'qa' to 'env_2'.
    When selecting an environment by name 'qa' from command line.
    Then a tuple containing the Env object for 'qa' and the string 'env_2' should be returned.
    """
    tool_envs = {"dev": "env_1", "qa": "env_2"}
    assert wax.select_env(envs, tool_envs, "qa") == (envs[1], "env_2")


def test_select_env_prompts_user_when_no_env_specified(monkeypatch, env_mock):
    """
    Given a list of environments and a tool_envs dictionary mapping 'dev' to 'env_1'.
    When no environment is specified in command line.
    Then user should be prompted to select an environment with a fuzzy search interface.
    And a tuple containing the Env object for 'dev' and the string 'env_1' should be returned.
    And this return value is based on the user's selection.
    """
    tool_envs = {"dev": "env_1", "qa": "env_2"}
    monkeypatch.setattr(prompt, "fuzzy", env_mock)

    assert wax.select_env(envs, tool_envs) == (envs[0], "env_1")
    assert env_mock.args[0] == "action.support.wax.select_environment"
    assert env_mock.args[1] == [
        {"value": "dev", "name": "dev"},
        {"value": "qa", "name": "qa"},
    ]
    assert env_mock.args[3] == "error.support.wax.invalid_environment"


def test_flatten_tools_for_list_view_with_no_groups():
    """
    Given a list of tools with no groups.
    When calling flatten_tools_for_list_view.
    Then the same tools should be returned with empty group context.
    """
    from hexagon.domain.tool import Tool

    tools = [
        Tool(name="tool1", type="shell", action="echo 1"),
        Tool(name="tool2", type="web", action="http://example.com"),
    ]
    flattened, context = wax.flatten_tools_for_list_view(tools)

    assert len(flattened) == 2
    assert flattened[0].name == "tool1"
    assert flattened[1].name == "tool2"
    assert context == {}


def test_flatten_tools_for_list_view_with_single_group():
    """
    Given a list of tools with one group containing nested tools.
    When calling flatten_tools_for_list_view.
    Then all tools and the group should be in the flattened list.
    And nested tools should have their group context set.
    """
    from hexagon.domain.tool import ActionTool, GroupTool

    nested_tools = [
        ActionTool(name="migrate", type="shell", action="migrate.sh"),
        ActionTool(name="rollback", type="shell", action="rollback.sh"),
    ]

    tools = [
        ActionTool(name="backup", type="shell", action="backup.sh"),
        GroupTool(
            name="database",
            long_name="Database Tools",
            type="group",
            tools=nested_tools,
        ),
    ]

    flattened, context = wax.flatten_tools_for_list_view(tools)

    # Should have: backup, database (group), migrate, rollback
    assert len(flattened) == 4
    assert flattened[0].name == "backup"
    assert flattened[1].name == "database"
    assert flattened[2].name == "migrate"
    assert flattened[3].name == "rollback"

    # Context should show group for nested tools
    assert context["migrate"] == "Database Tools"
    assert context["rollback"] == "Database Tools"
    assert "backup" not in context  # Top-level tool has no context


def test_flatten_tools_for_list_view_with_nested_groups():
    """
    Given a list of tools with nested groups (groups within groups).
    When calling flatten_tools_for_list_view.
    Then all tools should be flattened.
    And nested tools should show the full group path.
    """
    from hexagon.domain.tool import ActionTool, GroupTool

    innermost_tools = [
        ActionTool(name="run", type="shell", action="run.sh"),
    ]

    middle_tools = [
        ActionTool(name="deploy", type="shell", action="deploy.sh"),
        GroupTool(
            name="migrations",
            long_name="Migrations",
            type="group",
            tools=innermost_tools,
        ),
    ]

    tools = [
        GroupTool(name="ops", long_name="Operations", type="group", tools=middle_tools),
    ]

    flattened, context = wax.flatten_tools_for_list_view(tools)

    # Should have: ops (group), deploy, run
    assert len(flattened) == 3
    assert flattened[0].name == "ops"
    assert flattened[1].name == "deploy"
    assert flattened[2].name == "run"

    # Context should show full path
    assert context["deploy"] == "Operations"
    assert context["run"] == "Operations → Migrations"

---
sidebar_position: 2
---

# Tool API

The `Tool` class and its subclasses represent the tools available in your CLI. This page documents the properties and methods of the `Tool` class and its subclasses.

## Tool Class Hierarchy

Hexagon defines several tool classes:

- `Tool`: Base class for all tools
  - `ActionTool`: Tools that perform actions (web, shell)
  - `GroupTool`: Tools that group other tools

## Tool Class

The `Tool` class is defined in `hexagon/domain/tool/__init__.py` and uses Pydantic for data validation.

```python
class Tool(BaseModel):
    name: str
    type: ToolType = ToolType.misc
    icon: Optional[str] = None
    alias: Optional[str] = None
    long_name: Optional[str] = None
    description: Optional[str] = None
    envs: Optional[Dict[str, Any]] = None
    traced: Optional[bool] = True
```

### Properties

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `name` | `str` | The name of the tool | Yes |
| `type` | `ToolType` | The type of the tool | No (defaults to `misc`) |
| `icon` | `Optional[str]` | Icon to display | No |
| `alias` | `Optional[str]` | Short alias for the tool | No |
| `long_name` | `Optional[str]` | Longer descriptive name | No |
| `description` | `Optional[str]` | Detailed description | No |
| `envs` | `Optional[Dict[str, Any]]` | Environment-specific configurations | No |
| `traced` | `Optional[bool]` | Whether to trace tool execution | No (defaults to `True`) |

## ToolType Enum

The `ToolType` enum defines the available tool types:

```python
class ToolType(str, Enum):
    misc = "misc"
    web = "web"
    shell = "shell"
    hexagon = "hexagon"
    group = "group"
    function = "function"
    separator = "separator"
```

## ActionTool Class

The `ActionTool` class represents tools that perform actions, such as opening web links or executing shell commands.

```python
class ActionTool(Tool):
    action: Union[str, List[str]]
```

### Properties

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `action` | `Union[str, List[str]]` | The action to perform | Yes |

### Methods

| Method | Description |
|--------|-------------|
| `executable_str` | Returns the action as a string, joining multiple actions with newlines |



## GroupTool Class

The `GroupTool` class represents tools that group other tools.

```python
class GroupTool(Tool):
    tools: Union[str, List[Union[ActionTool, GroupTool]]]
```

### Properties

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `tools` | `Union[str, List[Union[ActionTool, GroupTool]]]` | The tools in the group | Yes |

## Examples

### Web Tool

```python
from hexagon.domain.tool import ActionTool, ToolType

web_tool = ActionTool(
    name="docs",
    alias="d",
    long_name="Documentation",
    description="Open team documentation",
    type=ToolType.web,
    action="open_link",
    envs={
        "dev": "https://docs-dev.example.com",
        "prod": "https://docs.example.com"
    }
)
```

### Shell Tool

```python
from hexagon.domain.tool import ActionTool, ToolType

shell_tool = ActionTool(
    name="deploy",
    alias="dep",
    long_name="Deploy Service",
    description="Deploy the service",
    type=ToolType.shell,
    action="./scripts/deploy.sh"
)
```



### Group Tool

```python
from hexagon.domain.tool import GroupTool, ActionTool, ToolType

provision_tool = ActionTool(
    name="provision",
    alias="p",
    long_name="Provision Resources",
    type=ToolType.shell,
    action="./scripts/provision.sh"
)

teardown_tool = ActionTool(
    name="teardown",
    alias="t",
    long_name="Teardown Resources",
    type=ToolType.shell,
    action="./scripts/teardown.sh"
)

group_tool = GroupTool(
    name="infra",
    alias="i",
    long_name="Infrastructure",
    description="Infrastructure tools",
    type=ToolType.group,
    tools=[provision_tool, teardown_tool]
)
```

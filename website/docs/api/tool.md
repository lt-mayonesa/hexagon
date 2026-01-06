---
sidebar_position: 2
---

# Tool API

The `Tool` class and its subclasses represent the tools available in your CLI. This page documents the properties and methods of the `Tool` class and its subclasses.

## Tool Class Hierarchy

Hexagon defines several tool classes:

- `Tool`: Base class for all tools
  - `ActionTool`: Tools that perform actions (web, shell, custom Python)
  - `GroupTool`: Tools that group other tools
  - `FunctionTool`: Tools that execute Python functions directly (Note: Typically uses base `Tool` class with `type=ToolType.function`)

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

**Note on `tools` property:**
- When a **string**, it's treated as a path to an external YAML file containing tool definitions
- When a **list**, it's the inline tool definitions

## FunctionTool

Function tools execute Python callable functions directly. Unlike `ActionTool` which references modules or scripts, function tools hold a direct reference to a Python function.

### Configuration

Function tools are typically created programmatically rather than in YAML:

```python
from hexagon.domain.tool import Tool, ToolType

def my_function():
    """Custom function to execute."""
    print("Function executed!")
    return ["Operation completed successfully"]

function_tool = Tool(
    name="my-func",
    type=ToolType.function,
    function=my_function,
    description="Execute a custom Python function",
    icon="⚡"
)
```

### Properties

Function tools use the base `Tool` class with these specific properties:

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `name` | `str` | Tool name | Yes |
| `type` | `ToolType.function` | Must be `function` | Yes |
| `function` | `Callable` | Python function to execute | Yes |
| `description` | `str` | Tool description | No |
| `icon` | `str` | Icon to display | No |
| `alias` | `str` | Short alias | No |

### Use Cases

**1. Plugin-Generated Tools**

Plugins can dynamically create function tools:

```python
# my_plugin.py
from hexagon.domain.tool import Tool, ToolType
from hexagon.runtime.singletons import configuration

def refresh_cache():
    """Clear and refresh application cache."""
    # Cache clearing logic
    return ["Cache refreshed successfully"]

def main():
    """Plugin initialization."""
    # Create and add a function tool dynamically
    cache_tool = Tool(
        name="refresh-cache",
        type=ToolType.function,
        function=refresh_cache,
        description="Refresh application cache"
    )

    # Add tool to configuration
    # (Note: This requires accessing internal configuration APIs)
```

**2. Programmatic CLIs**

Build entire CLIs in Python without YAML:

```python
from hexagon.domain.tool import Tool, ToolType
from hexagon.domain.cli import Cli

def status():
    return ["System status: OK"]

def restart():
    return ["System restarted"]

cli = Cli(name="Admin", command="admin")
tools = [
    Tool(name="status", type=ToolType.function, function=status),
    Tool(name="restart", type=ToolType.function, function=restart)
]
```

**3. Testing**

Create temporary tools for testing:

```python
def test_tool_execution():
    def mock_tool():
        return ["Test result"]

    tool = Tool(
        name="test",
        type=ToolType.function,
        function=mock_tool
    )

    # Execute and verify
    result = tool.function()
    assert result == ["Test result"]
```

### Function Signature

Function tools should follow this signature:

```python
def my_function() -> Optional[List[str]]:
    """
    Execute the function logic.

    Returns:
        Optional list of strings to display as output.
        If None, no output is shown.
    """
    # Your logic here
    return ["Result line 1", "Result line 2"]
```

### Difference from ActionTool

| Aspect | ActionTool | FunctionTool |
|--------|------------|--------------|
| Definition | References modules/scripts/commands | Direct function reference |
| Configuration | Defined in YAML | Created programmatically |
| Resolution | Resolved at runtime (imports module) | Already has function reference |
| Arguments | Supports Args class & env_args | No built-in argument support |
| Use Case | User-defined tools | Dynamic/programmatic tools |

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

### Function Tool

```python
from hexagon.domain.tool import Tool, ToolType

def check_status():
    """Check system status."""
    # Your status check logic
    return [
        "System: Online",
        "CPU: 45%",
        "Memory: 2.1GB / 8GB",
        "Disk: 120GB / 500GB"
    ]

function_tool = Tool(
    name="status",
    alias="s",
    long_name="System Status",
    description="Check system status",
    type=ToolType.function,
    function=check_status,
    icon="📊"
)
```

## See Also

- [Tool Types Guide](../guides/tool-types) - Overview of all tool types
- [Custom Tools](../advanced/custom-tools) - Creating Python tools with main() function
- [Plugins Guide](../guides/plugins) - Dynamically creating tools with plugins

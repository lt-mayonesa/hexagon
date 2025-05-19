---
sidebar_position: 5
---

# Plugins

Hexagon supports plugins to extend its functionality. This guide explains how to create, configure, and use plugins in your CLI.

## Understanding Plugins

Plugins are Python modules that can extend Hexagon's functionality by:

- Adding new tool types
- Modifying the behavior of existing tools
- Adding new commands or options
- Integrating with external systems
- Customizing the user interface

## Configuring Plugins

To use plugins in your CLI, specify them in the `plugins` list in your configuration file:

```yaml
cli:
  name: My CLI
  command: mycli
  plugins:
    - my_plugin
    - another_plugin
```

Hexagon will look for these plugins in your `custom_tools_dir` or in the Python path.

## Creating a Plugin

To create a plugin, create a Python module with a `setup` function that will be called when Hexagon loads the plugin:

```python
# my_plugin.py

def setup(cli, tools, envs):
    """Set up the plugin.
    
    Args:
        cli: The CLI configuration
        tools: The list of tools
        envs: The list of environments
    """
    print("Setting up my_plugin...")
    # Your plugin initialization code here
```

### Plugin Hooks

Plugins can register hooks to execute code at specific points in Hexagon's lifecycle. Hexagon provides several hooks through the `HexagonHooks` class:

```python
from hexagon.support.hooks import HexagonHooks

def setup(cli, tools, envs):
    # Register a hook to run at the start of Hexagon
    HexagonHooks.start.register(my_start_function)
    
    # Register a hook to run at the end of Hexagon
    HexagonHooks.end.register(my_end_function)

def my_start_function():
    print("Hexagon is starting...")

def my_end_function():
    print("Hexagon is ending...")
```

### Adding Custom Tool Types

Plugins can add custom tool types by registering them with Hexagon:

```python
from hexagon.domain.tool import Tool, ToolType
from hexagon.runtime.execute.tool import register_tool_executor

class MyCustomTool(Tool):
    custom_property: str

def execute_my_custom_tool(tool, env=None):
    print(f"Executing custom tool: {tool.name}")
    print(f"Custom property: {tool.custom_property}")
    return ["Custom tool executed successfully"]

def setup(cli, tools, envs):
    # Register the custom tool type
    ToolType.custom = "custom"
    
    # Register the executor for the custom tool type
    register_tool_executor(ToolType.custom, execute_my_custom_tool)
```

## Plugin Best Practices

- **Single Responsibility**: Each plugin should have a single, clear responsibility
- **Documentation**: Document your plugin's purpose, configuration, and usage
- **Error Handling**: Handle errors gracefully to avoid breaking the CLI
- **Compatibility**: Clearly specify which versions of Hexagon your plugin is compatible with
- **Testing**: Write tests for your plugin to ensure it works correctly

## Example Plugins

Here are some examples of what you can do with plugins:

### Logging Plugin

```python
# logging_plugin.py
import logging
from hexagon.support.hooks import HexagonHooks

def setup(cli, tools, envs):
    # Configure logging
    logging.basicConfig(filename="hexagon.log", level=logging.INFO)
    
    # Register hooks
    HexagonHooks.start.register(log_start)
    HexagonHooks.end.register(log_end)

def log_start():
    logging.info("Hexagon started")

def log_end():
    logging.info("Hexagon ended")
```

### Authentication Plugin

```python
# auth_plugin.py
from hexagon.support.hooks import HexagonHooks

def setup(cli, tools, envs):
    HexagonHooks.start.register(check_auth)

def check_auth():
    # Check if the user is authenticated
    if not is_authenticated():
        print("You are not authenticated. Please log in.")
        login()

def is_authenticated():
    # Check if the user is authenticated
    # This is just an example, implement your own authentication logic
    return False

def login():
    # Implement your login logic
    print("Logging in...")
```

## Next Steps

Learn about more advanced topics in the [Advanced](../advanced/custom-tools) section.

---
sidebar_position: 2
---

# Hooks API

Hexagon provides a hooks system that allows you to execute code at specific points in the CLI lifecycle. This page documents the hooks API and how to use it in your custom tools and plugins.

## HexagonHooks Class

The `HexagonHooks` class is defined in `hexagon/support/hooks.py` and provides access to the available hooks:

```python
from hexagon.support.hooks import HexagonHooks

# Register a function with the start hook
HexagonHooks.start.register(my_start_function)

# Register a function with the end hook
HexagonHooks.end.register(my_end_function)
```

## Available Hooks

Hexagon provides several built-in hooks:

| Hook | Description | When It's Called |
|------|-------------|------------------|
| `start` | Called when Hexagon starts | After initialization, before tool execution |
| `tool_selected` | Called when a tool is selected | After tool selection, before environment selection |
| `env_selected` | Called when an environment is selected | After environment selection, before tool execution |
| `before_tool_executed` | Called before a tool is executed | After environment selection, before tool execution |
| `tool_executed` | Called after a tool is executed | After tool execution, before exit |
| `end` | Called when Hexagon ends | After tool execution, before exit |

## Registering Hook Functions

To register a function with a hook, use the `register` method:

```python
from hexagon.support.hooks import HexagonHooks

def my_start_function():
    print("Hexagon is starting...")

# Register the function with the start hook
HexagonHooks.start.register(my_start_function)
```

## Hook Function Parameters

Hook functions can accept parameters that Hexagon will provide:

```python
def my_start_function(cli, tools, envs):
    print(f"Starting CLI: {cli.name}")
    print(f"Number of tools: {len(tools)}")
    print(f"Number of environments: {len(envs)}")
```

The available parameters depend on the hook. The `start` and `end` hooks provide `cli`, `tools`, and `envs` parameters.

## Hook Registration in Plugins

Hooks are typically registered in a plugin's `setup` function:

```python
# my_plugin.py
from hexagon.support.hooks import HexagonHooks

def setup(cli, tools, envs):
    HexagonHooks.start.register(my_start_function)
    HexagonHooks.end.register(my_end_function)

def my_start_function():
    print("Hexagon is starting...")

def my_end_function():
    print("Hexagon is ending...")
```

## Examples

### Logging Hook

```python
# logging_plugin.py
import logging
import time
from hexagon.support.hooks import HexagonHooks

def setup(cli, tools, envs):
    # Configure logging
    logging.basicConfig(filename="hexagon.log", level=logging.INFO)
    
    # Register hooks
    HexagonHooks.start.register(log_start)
    HexagonHooks.end.register(log_end)

def log_start():
    global start_time
    start_time = time.time()
    logging.info(f"Hexagon started at {time.strftime('%Y-%m-%d %H:%M:%S')}")

def log_end():
    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Hexagon ended at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Duration: {duration:.2f} seconds")
```

### Authentication Hook

```python
# auth_plugin.py
from hexagon.support.hooks import HexagonHooks
from hexagon.domain.hexagon_error import HexagonError

def setup(cli, tools, envs):
    HexagonHooks.start.register(check_auth)

def check_auth():
    # Check if the user is authenticated
    if not is_authenticated():
        # Prompt for authentication
        if not authenticate():
            # If authentication fails, raise an error to stop execution
            raise HexagonError("Authentication failed")

def is_authenticated():
    # Check if the user is authenticated
    # This is just an example, implement your own authentication logic
    return False

def authenticate():
    # Implement your authentication logic
    print("Please enter your credentials:")
    username = input("Username: ")
    password = input("Password: ")
    
    # Validate credentials
    # This is just an example, implement your own validation logic
    return username == "admin" and password == "password"
```

## Best Practices

- **Keep Hook Functions Simple**: Hook functions should be small and focused
- **Handle Errors**: Handle errors in hook functions to avoid breaking the CLI
- **Document Your Hooks**: Document what your hook functions do and when they're called
- **Use Appropriate Hooks**: Choose the right hook for your use case
- **Be Mindful of Performance**: Hook functions can impact CLI performance, so keep them efficient

---
sidebar_position: 2
---

# Hooks

Hexagon provides a hooks system that allows you to execute code at specific points in the CLI lifecycle. This guide explains how to use hooks to extend your CLI's functionality.

## Understanding Hooks

Hooks are points in Hexagon's execution flow where you can register functions to be called. They allow you to add custom behavior without modifying Hexagon's core code.

## Available Hooks

Hexagon provides several built-in hooks:

| Hook | Description | When It's Called |
|------|-------------|------------------|
| `start` | Called when Hexagon starts | After initialization, before tool execution |
| `end` | Called when Hexagon ends | After tool execution, before exit |

## Using Hooks

You can register functions with hooks in your custom tools or plugins:

```python
from hexagon.support.hooks import HexagonHooks

# Register a function with the start hook
HexagonHooks.start.register(my_start_function)

# Register a function with the end hook
HexagonHooks.end.register(my_end_function)

def my_start_function():
    print("Hexagon is starting...")

def my_end_function():
    print("Hexagon is ending...")
```

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

## Hook Execution Order

Functions registered with a hook are called in the order they were registered. If multiple plugins register functions with the same hook, the order depends on the order in which the plugins are loaded.

## Hook Function Parameters

Hook functions can accept parameters that Hexagon will provide:

```python
def my_start_function(cli, tools, envs):
    print(f"Starting CLI: {cli.name}")
    print(f"Number of tools: {len(tools)}")
    print(f"Number of environments: {len(envs)}")
```

The available parameters depend on the hook. Check the Hexagon documentation for details on each hook's parameters.

## Example: Logging Hook

Here's an example of using hooks to add logging to your CLI:

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

## Example: Authentication Hook

Here's an example of using hooks to add authentication to your CLI:

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

## Next Steps

Learn about [Internationalization](internationalization) to make your CLI accessible to users in different languages.

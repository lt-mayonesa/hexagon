---
sidebar_position: 2
---

# Hooks API

Hexagon provides a hooks system that allows you to execute code at specific points in the CLI lifecycle. This page documents the hooks API and how to use it in your custom tools and plugins.

## HexagonHooks Class

The `HexagonHooks` class is defined in `hexagon/support/hooks/__init__.py` and provides access to the available hooks:

```python
from hexagon.support.hooks import HexagonHooks
from hexagon.support.hooks.hook import HookSubscription

# Subscribe to the start hook
HexagonHooks.start.subscribe(
    HookSubscription("my-start-hook", callback=my_start_function)
)

# Subscribe to the end hook
HexagonHooks.end.subscribe(
    HookSubscription("my-end-hook", callback=my_end_function)
)
```

## Available Hooks

Hexagon provides six lifecycle hooks:

| Hook | Description | When It's Called | Data Type |
|------|-------------|------------------|-----------|
| `start` | Called when Hexagon starts | At the beginning of execution | `None` |
| `tool_selected` | Called when a tool is selected | After tool selection | `Selection[Tool]` |
| `env_selected` | Called when an environment is selected | After environment selection | `Selection[Env]` |
| `before_tool_executed` | Called before a tool is executed | Before tool execution | `ToolExecutionParameters` |
| `tool_executed` | Called after a tool is executed | After tool execution completes | `ToolExecutionData` |
| `end` | Called when Hexagon ends | At the end of execution | `None` |

## Hook Subscription

To subscribe to a hook, use the `HookSubscription` class:

```python
from hexagon.support.hooks import HexagonHooks
from hexagon.support.hooks.hook import HookSubscription, HookSubscrptionType

def my_callback(data=None):
    """Hook callback function.

    Args:
        data: Hook-specific data (None for start/end hooks)
    """
    print(f"Hook called with data: {data}")

# Create a subscription
subscription = HookSubscription(
    "unique-hook-id",                    # Unique identifier for this subscription
    callback=my_callback,                # Function to call
    type=HookSubscrptionType.sync        # Optional: sync (default) or background
)

# Subscribe to a hook
HexagonHooks.start.subscribe(subscription)
```

### HookSubscrptionType

Hooks can run in two modes:

- **`HookSubscrptionType.sync`** (default): Hook runs synchronously, blocking execution
- **`HookSubscrptionType.background`**: Hook runs in a background thread

```python
from hexagon.support.hooks.hook import HookSubscription, HookSubscrptionType

# Background hook (non-blocking)
HexagonHooks.tool_executed.subscribe(
    HookSubscription(
        "telemetry-reporter",
        callback=send_telemetry,
        type=HookSubscrptionType.background
    )
)
```

## Hook Data Types

### Selection[T]

Used by `tool_selected` and `env_selected` hooks:

```python
from hexagon.domain.hooks.wax import Selection, SelectionType

def on_tool_selected(selection: Selection):
    print(f"Tool selected: {selection.value.name}")
    print(f"Selection type: {selection.selection_type}")  # prompt or args

HexagonHooks.tool_selected.subscribe(
    HookSubscription("tool-logger", callback=on_tool_selected)
)
```

**Properties:**
- `value`: The selected tool or environment object
- `selection_type`: How it was selected (`SelectionType.prompt` or `SelectionType.args`)

### ToolExecutionParameters

Used by `before_tool_executed` hook:

```python
def on_before_execution(params):
    print(f"Executing tool: {params.tool.name}")
    print(f"Environment: {params.env.name if params.env else 'None'}")
    print(f"Environment args: {params.parameters}")
    print(f"CLI arguments: {params.arguments}")

HexagonHooks.before_tool_executed.subscribe(
    HookSubscription("pre-exec-logger", callback=on_before_execution)
)
```

**Properties:**
- `tool`: The `ActionTool` being executed
- `parameters`: Environment-specific parameters (`env_args`)
- `env`: The selected `Env` object (or `None`)
- `arguments`: Parsed CLI arguments

### ToolExecutionData

Used by `tool_executed` hook:

```python
def on_after_execution(data):
    print(f"Tool executed: {data.tool.name}")
    print(f"Duration: {data.duration:.2f}s")
    print(f"Environment args: {data.tool_env_args}")

HexagonHooks.tool_executed.subscribe(
    HookSubscription("post-exec-logger", callback=on_after_execution)
)
```

**Properties:**
- `tool`: The `ActionTool` that was executed
- `tool_env_args`: Environment-specific arguments used
- `duration`: Execution time in seconds

## Hook Registration in Plugins

Hooks are typically registered in a plugin's `main` function:

```python
# my_plugin.py
from hexagon.support.hooks import HexagonHooks
from hexagon.support.hooks.hook import HookSubscription

def main():
    """Plugin initialization function."""
    HexagonHooks.start.subscribe(
        HookSubscription("plugin-start", callback=on_start)
    )
    HexagonHooks.end.subscribe(
        HookSubscription("plugin-end", callback=on_end)
    )

def on_start():
    print("Hexagon is starting...")

def on_end():
    print("Hexagon is ending...")
```

## Examples

### Logging Hook

```python
# logging_plugin.py
import logging
import time
from hexagon.support.hooks import HexagonHooks
from hexagon.support.hooks.hook import HookSubscription

start_time = None

def main():
    # Configure logging
    logging.basicConfig(filename="hexagon.log", level=logging.INFO)

    # Register hooks
    HexagonHooks.start.subscribe(
        HookSubscription("log-start", callback=log_start)
    )
    HexagonHooks.tool_executed.subscribe(
        HookSubscription("log-execution", callback=log_execution)
    )
    HexagonHooks.end.subscribe(
        HookSubscription("log-end", callback=log_end)
    )

def log_start():
    global start_time
    start_time = time.time()
    logging.info(f"Hexagon started at {time.strftime('%Y-%m-%d %H:%M:%S')}")

def log_execution(data):
    logging.info(f"Executed tool: {data.tool.name} in {data.duration:.2f}s")

def log_end():
    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Hexagon ended at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Total duration: {duration:.2f} seconds")
```

### Authentication Hook

```python
# auth_plugin.py
from hexagon.support.hooks import HexagonHooks
from hexagon.support.hooks.hook import HookSubscription
from hexagon.domain.hexagon_error import HexagonError

def main():
    HexagonHooks.start.subscribe(
        HookSubscription("auth-check", callback=check_auth)
    )

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

### Tool Usage Tracking

```python
# usage_tracker.py
from hexagon.support.hooks import HexagonHooks
from hexagon.support.hooks.hook import HookSubscription, HookSubscrptionType
from hexagon.support.storage import store_user_data, load_user_data

def main():
    # Track tool usage in the background (non-blocking)
    HexagonHooks.tool_executed.subscribe(
        HookSubscription(
            "usage-tracker",
            callback=track_usage,
            type=HookSubscrptionType.background
        )
    )

def track_usage(data):
    """Track tool usage statistics."""
    tool_name = data.tool.name

    # Load existing stats
    stats = load_user_data("usage_stats") or {}

    # Update count
    stats[tool_name] = stats.get(tool_name, 0) + 1

    # Save updated stats
    store_user_data("usage_stats", stats)

    print(f"Tool '{tool_name}' has been used {stats[tool_name]} times")
```

## Best Practices

- **Keep Hook Functions Simple**: Hook functions should be small and focused
- **Handle Errors**: Handle errors in hook functions to avoid breaking the CLI
- **Document Your Hooks**: Document what your hook functions do and when they're called
- **Use Appropriate Hooks**: Choose the right hook for your use case
- **Be Mindful of Performance**: Synchronous hooks block execution, use background hooks for non-critical tasks
- **Unique Hook IDs**: Use descriptive, unique IDs for hook subscriptions to avoid conflicts

## See Also

- [Plugins Guide](../../guides/plugins) - Learn how to create plugins
- [Storage API](storage) - Store and retrieve user data
- [Hooks Domain Types](https://github.com/lt-mayonesa/hexagon/tree/main/hexagon/domain/hooks) - Full type definitions

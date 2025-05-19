---
sidebar_position: 3
---

# Storage API

Hexagon provides a storage system for persisting data between CLI invocations. This page documents the storage API and how to use it in your custom tools and plugins.

## Storage Module

The `hexagon.support.storage` module provides functions for storing and retrieving data:

```python
from hexagon.support.storage import (
    store_user_data,
    get_user_data,
    HexagonStorageKeys
)

# Store data
store_user_data("my_key", "my_value")

# Retrieve data
value = get_user_data("my_key")
print(value)  # "my_value"
```

## Storage Functions

### store_user_data

Stores a value with the specified key:

```python
from hexagon.support.storage import store_user_data

store_user_data("my_key", "my_value")
```

### get_user_data

Retrieves a value with the specified key:

```python
from hexagon.support.storage import get_user_data

value = get_user_data("my_key")
print(value)  # "my_value"
```

If the key doesn't exist, `get_user_data` returns `None` by default. You can specify a default value to return instead:

```python
value = get_user_data("non_existent_key", default="default_value")
print(value)  # "default_value"
```

## HexagonStorageKeys

Hexagon defines a set of standard storage keys in the `HexagonStorageKeys` enum:

```python
from hexagon.support.storage import HexagonStorageKeys

# Store the last command
store_user_data(HexagonStorageKeys.last_command.value, "my-cli tool")

# Retrieve the last command
last_command = get_user_data(HexagonStorageKeys.last_command.value)
print(last_command)  # "my-cli tool"
```

## Storage Location

Hexagon stores data in a JSON file in the user's home directory. The location depends on the operating system:

- **Linux/macOS**: `~/.hexagon/storage.json`
- **Windows**: `%USERPROFILE%\.hexagon\storage.json`

## Examples

### Storing User Preferences

```python
from hexagon.support.storage import store_user_data, get_user_data

def set_preference(key, value):
    """Set a user preference."""
    store_user_data(f"preference.{key}", value)
    return [f"Preference '{key}' set to '{value}'"]

def get_preference(key):
    """Get a user preference."""
    value = get_user_data(f"preference.{key}", default="Not set")
    return [f"Preference '{key}' is '{value}'"]
```

### Storing Tool State

```python
from hexagon.support.storage import store_user_data, get_user_data
import json

def save_state(state):
    """Save tool state."""
    store_user_data("tool_state", json.dumps(state))
    return ["State saved"]

def load_state():
    """Load tool state."""
    state_json = get_user_data("tool_state")
    if state_json:
        state = json.loads(state_json)
        return [f"State loaded: {state}"]
    else:
        return ["No state found"]
```

### Tracking Tool Usage

```python
from hexagon.support.storage import store_user_data, get_user_data
from hexagon.support.hooks import HexagonHooks
import json
import time

def setup(cli, tools, envs):
    HexagonHooks.end.register(track_usage)

def track_usage(cli, tools, envs, selected_tool=None):
    if not selected_tool:
        return
    
    # Get existing usage data
    usage_json = get_user_data("tool_usage", default="{}")
    usage = json.loads(usage_json)
    
    # Update usage data
    tool_name = selected_tool.name
    if tool_name not in usage:
        usage[tool_name] = 0
    usage[tool_name] += 1
    
    # Store updated usage data
    store_user_data("tool_usage", json.dumps(usage))
```

## Best Practices

- **Use Namespaced Keys**: Prefix your keys with a namespace to avoid conflicts
- **Handle Missing Data**: Always handle the case where data doesn't exist
- **Store Simple Data**: Store simple data types or JSON-serializable objects
- **Document Your Storage**: Document what data you store and why
- **Clean Up**: Remove data when it's no longer needed

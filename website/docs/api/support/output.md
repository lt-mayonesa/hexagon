---
sidebar_position: 1
---

# Output API

Hexagon provides a powerful output system for displaying information to users. This page documents the output API and how to use it in your custom tools and plugins.

## Printer Module

The `hexagon.support.output.printer` module provides functions for outputting information to the console. The main interface is the `log` object, which provides methods for different types of output.

```python
from hexagon.support.output.printer import log

# Basic output
log.info("This is an informational message")

# Result output (for command results)
log.result("Command output")

# Error message
log.error("An error occurred")

# Panel for highlighted information
log.panel("Important information")

# Start and finish messages
log.start("Starting operation")
log.finish("Operation complete")
```

## Output Methods

The `log` object provides several methods for different types of output:

| Method | Description |
|--------|-------------|
| `info` | Display an informational message |
| `result` | Display command result output |
| `error` | Display an error message |
| `panel` | Display a highlighted panel with content |
| `example` | Display code examples with syntax highlighting |
| `file` | Display file contents with syntax highlighting |
| `extra` | Display additional information |
| `start` | Display a start message (typically at CLI start) |
| `finish` | Display a finish message (typically at CLI end) |
| `gap` | Add a blank line |
| `status` | Show a progress status indicator |

## Themes

Hexagon supports different themes for output. The theme can be set using the `HEXAGON_THEME` environment variable or in the CLI configuration.

```python
from hexagon.support.output.printer import log

# Load a theme
log.load_theme("default")

# Available themes: default, disabled, result_only
```

## Internationalization

The printer module also provides the `_` function for internationalization:

```python
from hexagon.support.output.printer import _

# Mark a string for translation
message = _("Hello, World!")
print(message)
```

## Examples

### Basic Output

```python
from hexagon.support.output.printer import log

def my_function():
    log.info("Starting operation...")
    
    # Your logic here
    
    log.success("Operation completed successfully")
    return ["Result 1", "Result 2"]
```

### Error Handling

```python
from hexagon.support.output.printer import log

def risky_operation():
    try:
        # Your risky code here
        log.success("Operation successful")
        return ["Operation successful"]
    except Exception as e:
        log.error(f"Error: {str(e)}")
        return [f"Error: {str(e)}"]  # Return error message as output
```

### Internationalization

```python
from hexagon.support.output.printer import _, log

def greet(name):
    greeting = _("Hello, {name}!")
    message = greeting.format(name=name)
    log.info(message)
    return [message]
```

## Best Practices

- **Use Appropriate Methods**: Use the appropriate log method for the type of message
- **Be Consistent**: Use a consistent style for your output messages
- **Use Internationalization**: Mark user-facing strings for translation
- **Keep Messages Clear**: Write clear, concise messages
- **Handle Errors Gracefully**: Use error messages to provide helpful information when things go wrong

---
sidebar_position: 1
---

# Custom Tools

Hexagon allows you to create custom tools with Python code. This guide explains how to create and use custom tools in your CLI.

Custom tools are a core feature of Hexagon, allowing you to implement complex functionality that goes beyond simple shell commands or web links. They are Python modules that can be referenced directly in your CLI configuration.

## Understanding Custom Tools

Custom tools are Python modules that integrate with Hexagon's core functionality. They allow you to implement complex logic, interactive prompts, and rich terminal output that goes beyond simple shell commands or web links.

All custom Python tools follow a standard pattern:
1. Define an `Args` class for command-line arguments (optional)
2. Implement a `main(tool, env, env_args, cli_args)` function
3. Reference the module in your CLI configuration

## Creating a Custom Tool

### Step 1: Set Up Your Custom Tools Directory

Specify a `custom_tools_dir` in your CLI configuration:

```yaml
cli:
  name: My CLI
  command: mycli
  custom_tools_dir: ./custom_tools  # relative to the config file
```

This directory will be added to Python's import path, allowing Hexagon to find your modules.

### Step 2: Create a Python Module

Create a Python module with the standard tool structure:

```python
# custom_tools/greeting_tool.py
from hexagon.support.output.printer import log
from hexagon.support.input.args import ToolArgs, PositionalArg, OptionalArg, Arg

class Args(ToolArgs):
    """Define command-line arguments for this tool."""
    name: PositionalArg[str] = Arg(
        None,
        prompt_message="Enter your name",
        description="The name to greet"
    )
    greeting: OptionalArg[str] = Arg(
        "Hello",
        alias="g",
        prompt_message="Enter a greeting",
        description="The greeting to use"
    )

def main(tool, env, env_args, cli_args: Args):
    """Main entry point for the tool.

    Args:
        tool: The ActionTool object from YAML configuration
        env: The selected Environment object (or None)
        env_args: Environment-specific arguments from tool.envs[env.name]
        cli_args: Parsed command-line arguments (Args instance)
    """
    # Prompt for name if not provided via command line
    if not cli_args.name.value:
        cli_args.name.prompt()

    # Access environment information
    env_name = env.name if env else "No environment"
    env_specific = env_args if env_args else {}

    # Log information messages
    log.info(f"Tool: {tool.name}")
    log.info(f"Environment: {env_name}")

    # Create the greeting message
    message = f"{cli_args.greeting.value}, {cli_args.name.value}!"

    # Return results (displayed with log.result())
    return [message, f"Environment args: {env_specific}"]
```

### YAML Configuration

To use this custom tool in your CLI, configure it as a shell tool that references the Python module:

```yaml
- name: greet
  alias: g
  long_name: Greeting
  description: Greet a person
  type: shell
  action: greeting_tool
```

You can also provide environment-specific parameters:

```yaml
- name: greet-env
  alias: ge
  long_name: Environment Greeting
  description: Greet a person with environment-specific settings
  type: shell
  action: greeting_tool
  envs:
    dev:
      language: "English"
      formal: false
    prod:
      language: "Spanish"
      formal: true
```

### Understanding the main() Function

Every custom tool must implement a `main()` function with this exact signature:

```python
def main(tool, env, env_args, cli_args):
    pass
```

#### Parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `tool` | `ActionTool` | The tool configuration object from YAML (name, alias, description, action, etc.) |
| `env` | `Env` or `None` | The selected environment object (None if no environment or wildcard "*") |
| `env_args` | `Any` | Environment-specific value from `tool.envs[env.name]` (can be string, list, dict, or any type) |
| `cli_args` | `Args` or `CliArgs` | Parsed command-line arguments. If you define an `Args` class, it will be this type; otherwise, a generic `CliArgs` object |

#### Return Value:

Custom tools should return:
- **List of strings**: Each string is displayed as a result line
- **None**: No explicit output (tool should use `log.info()`, `log.result()`, etc. directly)

```python
def main(tool, env, env_args, cli_args):
    # Return explicit results
    return [
        "Operation successful",
        "Processed 10 items",
        "Duration: 2.5s"
    ]

# Or use logging directly
def main(tool, env, env_args, cli_args):
    log.result("Operation successful")
    log.info(f"Processed {count} items")
    # No return value
```

### Accessing Argument Values

When working with the `Args` class, you have two ways to access values:

```python
# Option 1: .value property (explicit)
name = cli_args.name.value  # Returns the actual value

# Option 2: Direct access (for checking)
if cli_args.name:  # Checks if value exists (not None)
    name = cli_args.name.value
```

**Best Practice**: Always use `.value` to get the actual value. The argument object itself contains metadata and prompt methods.

```python
# Good
name = cli_args.name.value
log.info(f"Hello, {name}!")

# Not recommended - accessing the argument object itself
log.info(f"Hello, {cli_args.name}!")  # May not display correctly
```

### Using the Printer Module

Custom tools can use the `log` object from `hexagon.support.output.printer` to display information:

```python
from hexagon.support.output.printer import log

def main(tool, env, env_args, cli_args):
    # Display information messages
    log.info("Processing...")
    
    # Display a panel with highlighted information
    log.panel("Important information", title="Note")
    
    # Display example code
    log.example("print('Hello, World!')", syntax="python")
    
    # Return results
    return ["Operation completed successfully"]
```

## Example: Data Processing Tool

```python
# custom_tools/data_processor.py
import json
import os
from hexagon.support.output.printer import log
from hexagon.support.input.args import ToolArgs, PositionalArg, Arg

class Args(ToolArgs):
    file_path: PositionalArg[str] = Arg(
        None, prompt_message="Enter the path to the JSON file"
    )

def main(tool, env, env_args, cli_args):
    # Only prompt if the file path wasn't provided as a command-line argument
    if not cli_args.file_path.value:
        cli_args.file_path.prompt()
    
    log.info(f"Processing file: {cli_args.file_path.value}")
    
    if not os.path.exists(cli_args.file_path.value):
        log.error(f"File not found: {cli_args.file_path.value}")
        return [f"Error: File not found: {cli_args.file_path.value}"]
    
    try:
        with open(cli_args.file_path.value, 'r') as f:
            data = json.load(f)
        
        # Process the data
        item_count = len(data)
        categories = set(item['category'] for item in data if 'category' in item)
        
        log.info(f"Found {item_count} items")
        log.info(f"Found {len(categories)} categories")
        
        return [
            f"Processed {item_count} items",
            f"Found {len(categories)} categories: {', '.join(categories)}"
        ]
    except json.JSONDecodeError:
        log.error("Invalid JSON file")
        return ["Error: Invalid JSON file"]
    except Exception as e:
        log.error(f"Error: {str(e)}")
        return [f"Error: {str(e)}"]
```

## Error Handling

Always handle errors gracefully in your custom tools:

```python
from hexagon.domain.hexagon_error import HexagonError

def main(tool, env, env_args, cli_args):
    try:
        # Your tool logic
        result = perform_operation()
        return [f"Success: {result}"]

    except FileNotFoundError as e:
        # User-friendly error messages
        log.error(f"File not found: {e.filename}")
        return [f"Error: File '{e.filename}' does not exist"]

    except ValueError as e:
        # Specific error handling
        log.error(f"Invalid value: {str(e)}")
        raise HexagonError(f"Invalid input: {str(e)}")

    except Exception as e:
        # Catch-all for unexpected errors
        log.error(f"Unexpected error: {str(e)}")
        raise HexagonError(f"Operation failed: {str(e)}")
```

**Error Handling Strategies:**
- **Return error message**: Tool completes but shows error in output
- **Raise HexagonError**: Stops execution and displays error to user
- **Log and continue**: Use `log.error()` for warnings that don't stop execution

## Best Practices

### Code Organization
- **One tool per file**: Keep tools focused and maintainable
- **Descriptive names**: Use clear module and function names
- **Documentation**: Add docstrings to Args class and main() function
- **Type hints**: Use type annotations for better IDE support

### User Experience
- **Clear prompts**: Use descriptive `prompt_message` for arguments
- **Helpful descriptions**: Add `description` to all arguments
- **Progress feedback**: Use `log.info()` for long-running operations
- **Consistent output**: Return structured, readable results

### Performance
- **Lazy loading**: Import heavy dependencies inside main() if not always needed
- **Caching**: Use `hexagon.support.storage` to cache expensive operations
- **Background operations**: Consider using hooks with `HookSubscrptionType.background` for async work

### Security
- **Validate input**: Always validate user input before using it
- **Sensitive data**: Use `skip_trace=True` when prompting for passwords
- **File paths**: Validate and sanitize file paths before file operations

```python
# Example: Secure password handling
class Args(ToolArgs):
    password: PositionalArg[str] = Arg(None)

def main(tool, env, env_args, cli_args):
    # Prompt without tracing sensitive data
    if not cli_args.password.value:
        cli_args.password.prompt(skip_trace=True)

    # Use the password (it won't appear in replay)
    authenticate(cli_args.password.value)
```

## Examples from Hexagon Core

Hexagon includes several built-in custom tools in the `hexagon/actions` directory that demonstrate best practices:

- **`hexagon/actions/external/open_link.py`**: Opens URLs in the default browser
- **`hexagon/actions/internal/create_new_tool.py`**: Creates new tools with interactive prompts
- **`hexagon/actions/internal/install_cli.py`**: Installs a CLI with proper error handling
- **`hexagon/actions/internal/save_new_alias.py`**: Saves command aliases with storage API
- **`hexagon/actions/internal/replay.py`**: Replays last command using tracer

These tools show how to implement complex functionality, handle errors, and provide excellent user experience.

## Next Steps

- Learn about [Prompting](prompting) for advanced interactive features
- Explore [Hooks](hooks) to extend your CLI's functionality
- Check the [Output API](../api/support/output) for rich terminal output
- See [Storage API](../api/support/storage) for persisting data

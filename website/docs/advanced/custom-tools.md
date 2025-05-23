---
sidebar_position: 1
---

# Custom Tools

Hexagon allows you to create custom tools with Python code. This guide explains how to create and use custom tools in your CLI.

Custom tools are a core feature of Hexagon, allowing you to implement complex functionality that goes beyond simple shell commands or web links. They are Python modules that can be referenced directly in your CLI configuration.

## Understanding Custom Tools

Custom tools are Python functions that can be called from your CLI. They provide a way to implement complex logic that can't be easily expressed as a shell command or web link.

## Creating a Custom Tool

To create a custom tool, you need to:

1. Create a Python module in your `custom_tools_dir`
2. Define a function in that module
3. Reference the function in your CLI configuration

### Step 1: Set Up Your Custom Tools Directory

Specify a `custom_tools_dir` in your CLI configuration:

```yaml
cli:
  name: My CLI
  command: mycli
  custom_tools_dir: ./custom_tools  # relative to the config file
```

### Step 2: Create a Python Module

Create a Python file in your custom tools directory:

```python
# custom_tools/data_tools.py

def analyze_data():
    """Analyze data and return results."""
    print("Analyzing data...")
    
    # Your analysis logic here
    results = [
        "Analysis complete",
        "Found 3 issues",
        "Performance: 95%"
    ]
    
    return results
```

### Step 3: Reference the Tool in Your Configuration

Reference the custom tool in your CLI configuration:

```yaml
tools:
  - name: analyze
    alias: a
    long_name: Analyze Data
    description: Run data analysis
    type: shell
    action: data_tools.analyze_data
```

## Return Values

Custom tools should return a list of strings, which will be displayed as output in the CLI:

```python
def my_function():
    # Your logic here
    return ["Line 1 of output", "Line 2 of output"]
```

If your function doesn't return anything, Hexagon will display a default success message.

## Accepting Arguments

You can define functions that accept arguments, which will be passed from the command line:

```python
def greet(name):
    """Greet a person by name."""
    return [f"Hello, {name}!"]
```

In your configuration:

```yaml
tools:
  - name: greet
    alias: g
    long_name: Greet
    description: Greet a person
    type: shell
    action: greetings.greet
```

Users can then pass arguments when calling the tool:

```bash
mycli greet John
```

## Accessing CLI Context

You can access the CLI context by defining a function that accepts specific parameters:

```python
def show_context(cli, tools, envs, env=None):
    """Show the CLI context."""
    output = [
        f"CLI Name: {cli.name}",
        f"CLI Command: {cli.command}",
        f"Number of Tools: {len(tools)}",
        f"Number of Environments: {len(envs)}",
    ]
    
    if env:
        output.append(f"Current Environment: {env.name}")
    
    return output
```

Hexagon will automatically pass the `cli`, `tools`, `envs`, and `env` parameters if your function defines them.

## Error Handling

You should handle errors in your functions to provide a good user experience:

```python
def risky_operation():
    """Perform a risky operation."""
    try:
        # Your risky code here
        return ["Operation successful"]
    except Exception as e:
        return [f"Error: {str(e)}"]  # Return error message as output
```

## Best Practices

- **Documentation**: Add docstrings to your functions to document their purpose and usage
- **Error Handling**: Handle errors gracefully to provide a good user experience
- **Return Values**: Return a list of strings for consistent output formatting
- **Modularity**: Keep functions small and focused on a single task
- **Testing**: Write tests for your custom tools to ensure they work correctly

## Creating Custom Python Tools

Hexagon's core functionality includes the ability to create custom tools that integrate directly with its core functionality. These tools are Python modules that can be referenced as shell actions in your CLI configuration.

### Tool Structure

A core-integrated custom tool typically consists of:

1. An `Args` class that defines the command-line arguments
2. A `main` function that implements the tool's functionality

```python
# custom_tools/greeting_tool.py
from hexagon.support.output.printer import log
from hexagon.support.input.args import ToolArgs, PositionalArg, OptionalArg, Arg

class Args(ToolArgs):
    name: PositionalArg[str] = Arg(
        None, prompt_message="Enter your name"
    )
    greeting: OptionalArg[str] = Arg(
        "Hello", prompt_message="Enter a greeting"
    )

def main(tool, env, env_args, cli_args):
    # Only prompt if the value wasn't provided as a command-line argument
    if not cli_args.name.value:
        cli_args.name.prompt()
    
    # Access the value directly from cli_args.name.value
    # No need to assign to a variable since cli_args.name holds the prompted value
    
    # Access environment-specific arguments if available
    env_name = env.name if env else "No environment"
    env_specific = env_args if env_args else {}
    
    # Log information messages
    log.info(f"Tool: {tool.name}")
    log.info(f"Environment: {env_name}")
    
    # Create the greeting message using values directly from cli_args
    message = f"{cli_args.greeting.value}, {cli_args.name.value}!"
    
    # Return results (will be displayed with log.result())
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

### Accessing the Tool Configuration

The `main` function receives four parameters:

1. `tool`: The tool configuration object (name, alias, description, etc.)
2. `env`: The selected environment object (if any)
3. `env_args`: Environment-specific arguments from the YAML configuration
4. `cli_args`: Command-line arguments defined in the `Args` class

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

## Examples from Hexagon Core

Hexagon includes several built-in custom tools in the `hexagon/actions` directory that demonstrate best practices:

- `hexagon/actions/external/open_link.py`: Opens URLs in the default browser
- `hexagon/actions/internal/create_new_tool.py`: Creates new tools with interactive prompts
- `hexagon/actions/internal/install_cli.py`: Installs a CLI with proper error handling

These tools show how to implement complex functionality, handle errors, and provide a good user experience.

## Next Steps

Learn how to use [Hooks](hooks) to extend your CLI's functionality further.

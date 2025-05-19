---
sidebar_position: 1
---

# Custom Tools

Hexagon allows you to create custom tools with Python code. This guide explains how to create and use custom tools in your CLI.

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

### Step 3: Reference the Function in Your Configuration

Reference the function in your CLI configuration:

```yaml
tools:
  - name: analyze
    alias: a
    long_name: Analyze Data
    description: Run data analysis
    type: function
    function: data_tools.analyze_data
```

The `function` property should be the module name and function name, separated by a dot.

## Function Return Values

Custom functions should return a list of strings, which will be displayed as output in the CLI:

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
    type: function
    function: greetings.greet
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

## Example: Data Processing Tool

```python
# custom_tools/data_processor.py
import json
import os

def process_data(file_path):
    """Process data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        List of strings with processing results
    """
    if not os.path.exists(file_path):
        return [f"Error: File not found: {file_path}"]
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Process the data
        item_count = len(data)
        categories = set(item['category'] for item in data if 'category' in item)
        
        return [
            f"Processed {item_count} items",
            f"Found {len(categories)} categories: {', '.join(categories)}"
        ]
    except json.JSONDecodeError:
        return ["Error: Invalid JSON file"]
    except Exception as e:
        return [f"Error: {str(e)}"]
```

## Next Steps

Learn how to use [Hooks](hooks) to extend your CLI's functionality further.

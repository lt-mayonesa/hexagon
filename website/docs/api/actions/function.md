---
sidebar_position: 3
---

# Function Actions

Function actions call Python functions. This page documents how to configure and use function actions in your CLI.

## Configuration

Function actions are configured using the `FunctionTool` class with `type` set to `function`:

```yaml
- name: analyze
  alias: a
  long_name: Analyze Data
  description: Run data analysis
  type: function
  function: custom_tools.analysis.analyze_data
```

The `function` property specifies the fully qualified function name. Hexagon will import the module and call the function when the tool is executed.

## Implementing Functions

To implement a function for a function tool, create a Python module in your `custom_tools_dir` with the function implementation:

```python
# custom_tools/analysis.py

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

Functions should return a list of strings, which will be displayed as output in the CLI. If a function doesn't return anything, Hexagon will display a default success message.

## Function Parameters

Functions can accept parameters, which will be passed from the command line:

```python
def greet(name):
    """Greet a person by name."""
    return [f"Hello, {name}!"]
```

When the tool is executed, Hexagon will prompt the user for the parameter values.

## Accessing CLI Context

Functions can access the CLI context by defining parameters with specific names:

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

## Examples

### Simple Function Tool

```yaml
- name: analyze
  alias: a
  long_name: Analyze Data
  description: Run data analysis
  type: function
  function: custom_tools.analysis.analyze_data
```

With implementation:

```python
# custom_tools/analysis.py

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

### Function Tool with Parameters

```yaml
- name: greet
  alias: g
  long_name: Greet
  description: Greet a person
  type: function
  function: custom_tools.greetings.greet
```

With implementation:

```python
# custom_tools/greetings.py

def greet(name):
    """Greet a person by name."""
    return [f"Hello, {name}!"]
```

### Function Tool with CLI Context

```yaml
- name: info
  alias: i
  long_name: CLI Info
  description: Show CLI information
  type: function
  function: custom_tools.info.show_info
```

With implementation:

```python
# custom_tools/info.py

def show_info(cli, tools, envs, env=None):
    """Show CLI information."""
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

## Best Practices

- **Keep Functions Simple**: Functions should have a single, clear responsibility
- **Handle Errors**: Handle errors gracefully to provide a good user experience
- **Return Values**: Return a list of strings for consistent output formatting
- **Documentation**: Add docstrings to your functions to document their purpose and usage
- **Testing**: Write tests for your functions to ensure they work correctly

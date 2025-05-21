---
sidebar_position: 2
---

# Tool Types

Hexagon supports several tool types, each designed for specific use cases. This guide explains each tool type and how to configure them.

One of Hexagon's core strengths is its ability to execute custom tools created in Python. This allows you to extend your CLI with powerful, custom functionality beyond the basic tool types.

## Web Tools

Web tools open URLs in your default browser. They're useful for accessing web applications, documentation, or any web resource.

### Configuration

```yaml
- name: docs
  alias: d
  long_name: Documentation
  description: Open team documentation
  type: web
  envs:
    dev: https://docs-dev.example.com
    prod: https://docs.example.com
  action: open_link
```

### Key Properties

- `type`: Must be set to `web`
- `action`: Must be set to `open_link`
- `envs`: Optional mapping of environment names to URLs

## Shell Tools

Shell tools execute shell commands. They're useful for running scripts, commands, or any CLI operation.

### Configuration

```yaml
- name: deploy
  alias: dep
  long_name: Deploy Service
  description: Deploy the service
  type: shell
  action: ./scripts/deploy.sh
```

### Multi-line Commands

For more complex commands, you can use a list of strings:

```yaml
- name: setup
  alias: s
  long_name: Setup Project
  description: Set up the project
  type: shell
  action:
    - "echo 'Setting up project...'" 
    - "npm install"
    - "npm run build"
```

### Key Properties

- `type`: Must be set to `shell`
- `action`: The shell command(s) to execute

## Function Tools

Function tools call Python functions. They're useful for implementing custom logic that can't be easily expressed as a shell command.

### Configuration

```yaml
- name: analyze
  alias: a
  long_name: Analyze Data
  description: Run data analysis
  type: function
  function: custom_tools.analysis.analyze_data
```

### Implementation

Create a Python file in your `custom_tools_dir` with the function implementation:

```python
# custom_tools/analysis.py

def analyze_data():
    print("Analyzing data...")
    # Your analysis logic here
    return ["Analysis complete", "Found 3 issues"]  # Return list of strings for output
```

### Key Properties

- `type`: Must be set to `function`
- `function`: The fully qualified function name

## Group Tools

Group tools organize related tools together. They're useful for creating a hierarchical structure in your CLI.

### Configuration

```yaml
- name: infra
  alias: i
  long_name: Infrastructure
  description: Infrastructure tools
  type: group
  tools:
    - name: provision
      alias: p
      long_name: Provision Resources
      type: shell
      action: ./scripts/provision.sh
    - name: teardown
      alias: t
      long_name: Teardown Resources
      type: shell
      action: ./scripts/teardown.sh
```

### Key Properties

- `type`: Must be set to `group`
- `tools`: List of tools in the group

## Separator

Separators add visual separation between tools in the CLI menu. They're useful for organizing tools into logical sections.

### Configuration

```yaml
- name: __separator
  type: separator
```

### Key Properties

- `type`: Must be set to `separator`
- `name`: Conventionally set to `__separator`

## Hexagon Tools

Hexagon tools are built-in tools provided by Hexagon itself. They're used for managing Hexagon and your custom CLIs.

### Configuration

These are typically not configured directly by users but are provided by Hexagon.

### Key Properties

- `type`: Set to `hexagon`

## Custom Python Tools

One of Hexagon's most powerful features is the ability to execute custom Python tools. These are Python modules that implement specific functionality and can be referenced directly in your CLI configuration.

### Configuration

Custom Python tools are typically configured as shell tools that reference a Python module:

```yaml
- name: custom-tool
  alias: ct
  long_name: Custom Tool
  description: Execute a custom Python tool
  type: shell
  action: python_module
```

You can also provide environment-specific parameters:

```yaml
- name: custom-tool-env
  alias: cte
  long_name: Custom Tool with Environment
  description: Execute a custom Python tool with environment-specific parameters
  type: shell
  action: python_module
  envs:
    dev:
      - param1
      - param2
    prod:
      param1: value1
      param2: value2
```

### Implementation

Custom Python tools are implemented as Python modules in the Hexagon codebase or in your custom tools directory. Here's a simplified example of a custom tool implementation:

```python
from hexagon.support.output.printer import log
from hexagon.support.input.args import ToolArgs, PositionalArg, Arg

class Args(ToolArgs):
    name: PositionalArg[str] = Arg(
        None, prompt_message="Enter a name"
    )

def main(tool, env, env_args, cli_args):
    # Access tool configuration
    tool_name = tool.name
    
    # Access environment
    env_name = env.name if env else "No environment"
    
    # Access environment-specific arguments
    env_specific_args = env_args
    
    # Only prompt for command-line arguments if not provided
    if not cli_args.name.value:
        cli_args.name.prompt()
    
    # Output results
    log.info(f"Executing {tool_name} in {env_name}")
    log.info(f"Hello, {cli_args.name.value}!")
    
    # Return results (displayed with log.result())
    return [
        f"Tool: {tool_name}",
        f"Environment: {env_name}",
        f"Environment Args: {env_specific_args}",
        f"Name: {cli_args.name.value}"
    ]
```

### Accessing Tool Configuration

Custom tools have access to:

- `tool`: The tool configuration (name, alias, description, etc.)
- `env`: The selected environment (if any)
- `env_args`: Environment-specific arguments from the YAML configuration
- `cli_args`: Command-line arguments defined in the `Args` class

### Examples in Hexagon Core

Hexagon includes several built-in custom tools in the `hexagon/actions` directory:

- `hexagon/actions/external/open_link.py`: Opens URLs in the default browser
- `hexagon/actions/internal/create_new_tool.py`: Creates new tools
- `hexagon/actions/internal/install_cli.py`: Installs a CLI

These tools demonstrate how to implement complex functionality that goes beyond simple shell commands or web links.

## Best Practices

- **Choose the Right Type**: Select the tool type that best fits your use case
- **Consistent Naming**: Use consistent naming conventions for tools and aliases
- **Clear Descriptions**: Provide clear descriptions for each tool
- **Organize with Groups**: Use groups to organize related tools
- **Use Separators**: Add separators to visually separate different sections of your CLI
- **Leverage Custom Tools**: Use custom Python tools for complex functionality

## Next Steps

Learn how to configure [Environments](environments) for your CLI.

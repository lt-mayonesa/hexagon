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

## Custom Python Tools

Custom Python tools allow you to implement complex logic with full access to Hexagon's APIs. These are Python modules with a `main(tool, env, env_args, cli_args)` function.

### How Hexagon Finds Python Modules

When you reference a Python module in the `action` field, Hexagon searches in this order:

1. **Custom tools directory**: Modules in your `custom_tools_dir`
2. **Built-in actions**: Modules in `hexagon.actions.external`

### Configuration

```yaml
- name: my-tool
  type: shell
  action: my_module  # Hexagon will find custom_tools/my_module.py
```

### Inline Commands with Format Strings

Shell actions support format string interpolation for dynamic values:

```yaml
- name: deploy
  type: shell
  action: "echo Deploying {tool.name} to {env.name} at {env_args}"
  envs:
    dev: "http://localhost:3000"
    prod: "https://prod.example.com"
```

**Available format variables:**
- `{tool.name}`, `{tool.alias}`, `{tool.type}` - Tool properties
- `{env.name}`, `{env.alias}` - Environment properties
- `{env_args}` - Environment-specific value
- `{cli_args}` - Extra command-line arguments

See the [Custom Tools](../advanced/custom-tools) documentation for complete details on creating Python tools.

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

## Function Tools

Function tools execute Python callable functions directly. Unlike custom Python tools that use modules, function tools reference Python functions that can be created programmatically or by plugins.

### Configuration

Function tools are typically created programmatically rather than in YAML:

```python
from hexagon.domain.tool import Tool, ToolType

def my_function():
    print("Function executed!")
    return ["Function completed"]

function_tool = Tool(
    name="my-func",
    type=ToolType.function,
    function=my_function,
    description="Execute a Python function"
)
```

### Key Properties

- `type`: Must be set to `function`
- `function`: A Python callable object

### Use Cases

- **Plugin-generated tools**: Plugins can dynamically create function tools
- **Programmatic CLIs**: Build tools entirely in Python without YAML
- **Testing**: Create temporary tools for testing purposes

## Hexagon Tools

Hexagon tools are built-in tools provided by Hexagon itself. They're used for managing Hexagon and your custom CLIs.

### Built-in Tools

Hexagon provides several built-in tools automatically:

**Initial Setup Tools** (available when running bare `hexagon` without config):
- `install` - Install a CLI from configuration
- `get-json-schema` - Get JSON schema for YAML validation
- `update-hexagon` - Update Hexagon framework

**Default Tools** (available in all CLI projects):
- `save-alias` - Save command aliases
- `replay` (alias: `r`) - Re-run last command
- `create-tool` - Interactive tool creation wizard
- `update-cli` - Update CLI from git repository

See the [Built-in Tools API](../api/built-in-tools) for complete documentation.

### Key Properties

- `type`: Set to `hexagon`
- These tools are automatically registered and don't need YAML configuration

## Script Execution

Shell tools can execute script files with automatic interpreter detection.

### Supported Script Types

| Extension | Interpreter | Example |
|-----------|-------------|---------|
| `.sh` | `sh` | `action: ./scripts/deploy.sh` |
| `.js` | `node` | `action: ./scripts/build.js` |

Script paths are relative to your project directory (where your config file is located).

### Environment Variables for Scripts

Shell scripts receive special environment variables:

```bash
#!/bin/bash
# scripts/my-script.sh

# Access tool configuration as JSON
echo $HEXAGON_EXECUTION_TOOL | jq '.name'

# Access environment configuration as JSON
echo $HEXAGON_EXECUTION_ENV | jq '.name'
```

See the [Shell Actions API](../api/actions/shell) for complete documentation.

## Best Practices

- **Choose the Right Type**: Select the tool type that best fits your use case
- **Consistent Naming**: Use consistent naming conventions for tools and aliases
- **Clear Descriptions**: Provide clear descriptions for each tool
- **Organize with Groups**: Use groups to organize related tools
- **Use Separators**: Add separators to visually separate different sections of your CLI
- **Leverage Custom Tools**: Use custom Python tools for complex functionality
- **Script Organization**: Keep scripts in a dedicated directory (e.g., `scripts/`)
- **Environment-Specific Values**: Use the `envs` field for environment-specific URLs, hosts, or parameters

## Tool Type Selection Guide

| Need | Recommended Type | Example |
|------|------------------|---------|
| Open a URL | `web` | Documentation, dashboards |
| Run a script | `shell` with script path | Deployment scripts, builds |
| Execute a command | `shell` with inline command | `git status`, `docker ps` |
| Complex logic | `shell` with Python module | Data processing, API calls |
| Dynamic commands | `shell` with format strings | Environment-specific commands |
| Organize tools | `group` | Database tools, deployment tools |
| Visual organization | `separator` | Section dividers |
| Programmatic tools | `function` | Plugin-generated tools |

## Next Steps

- Learn about [Environments](environments) for multi-environment configuration
- Explore [Custom Tools](../advanced/custom-tools) for building powerful Python tools
- See [Action Execution](../advanced/action-execution) to understand how Hexagon resolves and runs actions

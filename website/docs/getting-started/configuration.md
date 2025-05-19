---
sidebar_position: 3
---

# Configuration

Hexagon CLIs are configured using YAML files. This guide explains the structure and options available in the configuration file.

## Configuration File Structure

A Hexagon configuration file has three main sections:

- `cli`: Defines the CLI itself
- `envs`: Defines the environments your CLI supports
- `tools`: Defines the tools available in your CLI

Here's a basic example:

```yaml
cli:
  name: My CLI
  command: mycli
  custom_tools_dir: ./custom_tools
  plugins: []

envs:
  - name: development
    alias: dev
  - name: production
    alias: prod

tools:
  - name: tool1
    alias: t1
    type: web
    action: open_link
    envs:
      development: https://dev.example.com
      production: https://example.com
```

## CLI Configuration

The `cli` section defines the basic properties of your CLI:

| Property | Description | Required |
|----------|-------------|----------|
| `name` | The display name of your CLI | Yes |
| `command` | The command used to invoke your CLI | Yes |
| `custom_tools_dir` | Directory for custom tool implementations | No |
| `plugins` | List of plugins to use | No |
| `entrypoint.shell` | Custom shell to use for commands | No |
| `entrypoint.pre_command` | Command to run before each tool execution | No |
| `entrypoint.environ` | Environment variables to set | No |

## Environment Configuration

The `envs` section defines the environments your CLI supports:

| Property | Description | Required |
|----------|-------------|----------|
| `name` | The name of the environment | Yes |
| `alias` | Short alias for the environment | No |
| `long_name` | Longer descriptive name | No |
| `description` | Detailed description | No |

## Tool Configuration

The `tools` section defines the tools available in your CLI:

| Property | Description | Required |
|----------|-------------|----------|
| `name` | The name of the tool | Yes |
| `alias` | Short alias for the tool | No |
| `long_name` | Longer descriptive name | No |
| `description` | Detailed description | No |
| `type` | Tool type (web, shell, function, etc.) | Yes |
| `action` | The action to perform | Yes |
| `envs` | Environment-specific configurations | No |
| `icon` | Icon to display | No |
| `traced` | Whether to trace tool execution | No |

### Tool Types

Hexagon supports several tool types:

- `web`: Opens a web link
- `shell`: Executes a shell command
- `function`: Calls a Python function
- `group`: Groups multiple tools together
- `misc`: Miscellaneous tool type
- `hexagon`: Hexagon-specific tools
- `separator`: Visual separator in the CLI

## Configuration File Location

Hexagon looks for configuration files in several locations:

1. The path specified by the `HEXAGON_CONFIG_FILE` environment variable
2. A file named `hexagon_tools.yaml` in the current directory
3. A file named `hexagon_tools.yml` in the current directory

## Next Steps

Now that you understand how to configure your CLI, check out the [Creating a CLI](../guides/creating-a-cli) guide for a more detailed walkthrough.

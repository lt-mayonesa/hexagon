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
| `options` | Runtime options (theme, update settings, etc.) | No |
| `entrypoint.shell` | Custom shell to use for commands | No |
| `entrypoint.pre_command` | Command to run before each tool execution | No |
| `entrypoint.environ` | Environment variables to set | No |

### Runtime Options

The `options` section allows you to configure Hexagon's runtime behavior:

```yaml
cli:
  name: My CLI
  command: mycli
  options:
    theme: default                      # default, disabled, or result_only
    update_disabled: false              # Disable hexagon update checks
    cli_update_disabled: false          # Disable CLI update checks
    hints_disabled: false               # Disable hint messages
    cwd_tools_disabled: false           # Disable directory-specific tools
    send_telemetry: false               # Enable/disable telemetry
```

See the [Runtime Options API](../api/runtime-options) for a complete list of available options.

### Entrypoint Configuration

The `entrypoint` section allows you to customize the execution environment:

```yaml
cli:
  name: My CLI
  command: mycli
  entrypoint:
    shell: zsh                          # Shell to use (default: sh)
    pre_command: source ~/.env          # Command to run before each tool
    environ:                            # Environment variables
      NODE_ENV: production
      API_KEY: your-api-key
```

This is useful for:
- Loading environment-specific configurations
- Setting up authentication
- Initializing required environment variables

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

Hexagon looks for your main configuration file in the following order:

1. The path specified by the `HEXAGON_CONFIG_FILE` environment variable
2. A file named `app.yaml` in the current directory (default)
3. A file named `app.yml` in the current directory

### Current Working Directory Tools

In addition to your main configuration file, Hexagon can load directory-specific tools from `hexagon_tools.yaml` or `hexagon_tools.yml` in the current working directory. These tools are added to your CLI when running from that directory.

This feature is useful for project-specific tools that should only be available in certain directories. To disable this feature, set `cwd_tools_disabled: true` in your CLI options.

See the [Runtime Options](../api/runtime-options) documentation for more details.

## Next Steps

Now that you understand how to configure your CLI, check out the [Creating a CLI](../guides/creating-a-cli) guide for a more detailed walkthrough.

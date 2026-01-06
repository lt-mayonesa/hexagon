---
sidebar_position: 1
---

# CLI API

The `Cli` class is the core component that defines your custom CLI. This page documents the properties and methods of the `Cli` class.

## Cli Class

The `Cli` class is defined in `hexagon/domain/cli.py` and uses Pydantic for data validation.

```python
class Cli(BaseModel):
    name: str
    command: str
    entrypoint: EntrypointConfig = EntrypointConfig()
    custom_tools_dir: Optional[str] = None
    plugins: List[str] = []
    options: Optional[dict] = None
```

### Properties

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `name` | `str` | The display name of your CLI | Yes |
| `command` | `str` | The command used to invoke your CLI | Yes |
| `entrypoint` | `EntrypointConfig` | Configuration for the CLI entrypoint | No |
| `custom_tools_dir` | `Optional[str]` | Directory for custom tool implementations | No |
| `plugins` | `List[str]` | List of plugins to use | No |
| `options` | `Optional[dict]` | Runtime options (theme, updates, etc.) | No |

#### Property Details

**`name`**: The display name shown in menus and help text.

**`command`**: The command users type to invoke your CLI (e.g., `mycli` means users run `mycli`).

**`entrypoint`**: Customizes the execution environment. See [EntrypointConfig](#entrypointconfig-class) below.

**`custom_tools_dir`**: Path to a directory containing custom Python tools, relative to the config file. This directory is added to Python's sys.path, allowing tools to import custom modules.

**`plugins`**: List of plugin paths (relative to project directory). Plugins extend Hexagon with custom functionality. See [Plugins Guide](../guides/plugins).

**`options`**: Runtime configuration options. See [Runtime Options](#runtime-options) below.

## EntrypointConfig Class

The `EntrypointConfig` class defines how the CLI is executed.

```python
class EntrypointConfig(BaseModel):
    shell: Optional[str] = None
    pre_command: Optional[str] = None
    environ: Dict[str, Any] = {}
```

### Properties

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `shell` | `Optional[str]` | Custom shell to use for commands (default: `sh`) | No |
| `pre_command` | `Optional[str]` | Command to run before each tool execution | No |
| `environ` | `Dict[str, Any]` | Environment variables to set | No |

#### Entrypoint Use Cases

**Custom Shell**: Use a specific shell for command execution
```yaml
entrypoint:
  shell: zsh  # Use zsh instead of sh
```

**Environment Setup**: Run setup commands before each tool
```yaml
entrypoint:
  pre_command: source ~/.env && export PATH="$PATH:/custom/bin"
```

**Environment Variables**: Set variables for all tool executions
```yaml
entrypoint:
  environ:
    NODE_ENV: production
    API_KEY: your-api-key
    DEBUG: "false"
```

## Runtime Options

The `options` property configures Hexagon's runtime behavior. Options can be set in three ways (in order of precedence):

1. **YAML configuration** (`cli.options`)
2. **Environment variables** (prefix with `HEXAGON_`)
3. **User storage** (persisted settings)

### Available Options

```yaml
cli:
  options:
    # UI Configuration
    theme: default                          # default, disabled, result_only
    hints_disabled: false                   # Disable hint messages

    # Update Configuration
    update_disabled: false                  # Disable hexagon framework updates
    cli_update_disabled: false              # Disable CLI project updates
    update_time_between_checks: 86400       # Update check interval (seconds)

    # Feature Configuration
    send_telemetry: false                   # Enable/disable telemetry
    disable_dependency_scan: false          # Disable dependency scanning
    cwd_tools_disabled: false               # Disable directory-specific tools

    # Storage Configuration
    config_storage_path: /custom/path       # Custom storage location

    # Keyboard Configuration
    keymap:
      create_dir: "c-p"                     # Custom keyboard shortcuts
```

### Options Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `theme` | `str` | `"default"` | UI theme: `default`, `disabled`, `result_only` |
| `update_disabled` | `bool` | `false` | Disable automatic hexagon framework updates |
| `cli_update_disabled` | `bool` | `false` | Disable automatic CLI project updates |
| `update_time_between_checks` | `int` | `86400` | Seconds between update checks (1 day) |
| `hints_disabled` | `bool` | `false` | Disable helpful hint messages |
| `cwd_tools_disabled` | `bool` | `false` | Disable loading `hexagon_tools.yaml` from current directory |
| `send_telemetry` | `bool` | `false` | Enable anonymous usage telemetry |
| `disable_dependency_scan` | `bool` | `false` | Disable dependency vulnerability scanning |
| `config_storage_path` | `str` | System default | Custom path for user data storage |
| `keymap` | `dict` | `{}` | Custom keyboard shortcut mappings |

### Environment Variable Equivalents

All options can be set via environment variables by prefixing with `HEXAGON_`:

```bash
export HEXAGON_THEME=disabled
export HEXAGON_UPDATE_DISABLED=true
export HEXAGON_CLI_UPDATE_DISABLED=true
export HEXAGON_HINTS_DISABLED=true
export HEXAGON_CWD_TOOLS_DISABLED=true
export HEXAGON_SEND_TELEMETRY=false
```

### Theme Options

**`default`**: Full rich terminal output with colors, borders, and formatting

**`disabled`**: Minimal output without styling (useful for CI/CD)

**`result_only`**: Only show final results, hide intermediate messages

See the [Runtime Options API](runtime-options) for complete documentation.

## Complete Example

Here's a comprehensive example of a CLI configuration:

```yaml
cli:
  name: Team CLI
  command: team
  custom_tools_dir: ./custom_tools
  plugins:
    - plugins/telemetry.py
    - plugins/authentication.py

  options:
    theme: default
    update_disabled: false
    cli_update_disabled: false
    hints_disabled: false
    cwd_tools_disabled: false

  entrypoint:
    shell: zsh
    pre_command: source ~/.env
    environ:
      NODE_ENV: production
      DEBUG: "false"
```

And here's how you might create a `Cli` instance programmatically:

```python
from hexagon.domain.cli import Cli, EntrypointConfig

entrypoint = EntrypointConfig(
    shell="zsh",
    pre_command="source ~/.env",
    environ={
        "NODE_ENV": "production",
        "DEBUG": "false"
    }
)

cli = Cli(
    name="Team CLI",
    command="team",
    custom_tools_dir="./custom_tools",
    plugins=["plugins/telemetry.py", "plugins/authentication.py"],
    options={
        "theme": "default",
        "update_disabled": False,
        "hints_disabled": False
    },
    entrypoint=entrypoint
)
```

## See Also

- [Configuration Guide](../getting-started/configuration) - Complete YAML configuration reference
- [Runtime Options API](runtime-options) - Detailed options documentation
- [Plugins Guide](../guides/plugins) - Creating and using plugins
- [Theming Guide](../guides/theming) - UI theme customization

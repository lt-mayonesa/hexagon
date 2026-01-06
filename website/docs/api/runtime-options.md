---
sidebar_position: 6
---

# Runtime Options API

Runtime options configure Hexagon's behavior. This page documents all available options, how to set them, and what they control.

## Setting Options

Runtime options can be set in three ways (in order of precedence):

1. **YAML Configuration** - In your `app.yaml` file
2. **Environment Variables** - Using `HEXAGON_` prefix
3. **User Storage** - Persisted settings (lowest priority)

### YAML Configuration

```yaml
cli:
  name: My CLI
  command: mycli
  options:
    theme: default
    update_disabled: false
    hints_disabled: false
```

### Environment Variables

```bash
# Prefix all options with HEXAGON_
export HEXAGON_THEME=disabled
export HEXAGON_UPDATE_DISABLED=true
export HEXAGON_HINTS_DISABLED=true

# Then run your CLI
mycli
```

### Precedence Example

```yaml
# app.yaml
options:
  theme: default  # Value: default
```

```bash
# Override with environment variable
export HEXAGON_THEME=disabled  # Value: disabled (takes precedence)

mycli  # Uses theme: disabled
```

## All Runtime Options

### UI Options

#### theme

Controls the visual output style.

**Type:** `string`
**Default:** `"default"`
**Values:** `default`, `disabled`, `result_only`

```yaml
options:
  theme: default
```

**Themes:**

- **`default`**: Full rich terminal output with colors, borders, spinners, and formatting
- **`disabled`**: Minimal output without styling (good for CI/CD, logs, and piping)
- **`result_only`**: Only shows final results, hides status messages and prompts

**Environment variable:**
```bash
export HEXAGON_THEME=disabled
```

#### hints_disabled

Disables helpful hint messages.

**Type:** `boolean`
**Default:** `false`

```yaml
options:
  hints_disabled: false
```

When `false`, Hexagon shows helpful hints like:
- Keyboard shortcuts
- Available commands
- Tips for using features

When `true`, hints are hidden for a cleaner experience.

**Environment variable:**
```bash
export HEXAGON_HINTS_DISABLED=true
```

### Update Options

#### update_disabled

Disables automatic Hexagon framework update checks.

**Type:** `boolean`
**Default:** `false`

```yaml
options:
  update_disabled: false
```

When `false`, Hexagon checks for framework updates periodically and notifies you when a new version is available.

When `true`, no update checks are performed.

**Environment variable:**
```bash
export HEXAGON_UPDATE_DISABLED=true
```

#### cli_update_disabled

Disables automatic CLI project update checks.

**Type:** `boolean`
**Default:** `false`

```yaml
options:
  cli_update_disabled: false
```

When `false`, Hexagon checks if your CLI project (if it's a git repository) has updates available.

When `true`, no CLI update checks are performed.

**Environment variable:**
```bash
export HEXAGON_CLI_UPDATE_DISABLED=true
```

#### update_time_between_checks

Time in seconds between automatic update checks.

**Type:** `integer`
**Default:** `86400` (24 hours)

```yaml
options:
  update_time_between_checks: 86400  # Check daily
```

Set to `0` to check on every CLI invocation (not recommended).

**Common values:**
- `3600` - Every hour
- `86400` - Every day (default)
- `604800` - Every week
- `0` - Every run (not recommended)

**Environment variable:**
```bash
export HEXAGON_UPDATE_TIME_BETWEEN_CHECKS=604800
```

### Feature Options

#### cwd_tools_disabled

Disables loading tools from `hexagon_tools.yaml` in the current working directory.

**Type:** `boolean`
**Default:** `false`

```yaml
options:
  cwd_tools_disabled: false
```

When `false`, Hexagon automatically loads tools from `hexagon_tools.yaml` or `hexagon_tools.yml` in the current directory.

When `true`, directory-specific tools are ignored.

**Use case:** Disable when you want consistent tools across all directories.

**Environment variable:**
```bash
export HEXAGON_CWD_TOOLS_DISABLED=true
```

#### send_telemetry

Enables anonymous usage telemetry.

**Type:** `boolean`
**Default:** `false`

```yaml
options:
  send_telemetry: false
```

When `true`, Hexagon collects anonymous usage statistics to help improve the framework.

When `false`, no telemetry is collected.

**What's collected (when enabled):**
- Tool usage frequency
- Error occurrences
- Feature usage patterns
- NO personal data or command arguments

**Environment variable:**
```bash
export HEXAGON_SEND_TELEMETRY=true
```

#### disable_dependency_scan

Disables dependency vulnerability scanning.

**Type:** `boolean`
**Default:** `false`

```yaml
options:
  disable_dependency_scan: false
```

When `false`, Hexagon may scan dependencies for known vulnerabilities.

When `true`, dependency scanning is disabled.

**Environment variable:**
```bash
export HEXAGON_DISABLE_DEPENDENCY_SCAN=true
```

### Storage Options

#### config_storage_path

Custom path for storing user data and settings.

**Type:** `string`
**Default:** System-dependent

```yaml
options:
  config_storage_path: /custom/path/to/storage
```

**Default locations:**
- **Linux/macOS:** `~/.config/hexagon/`
- **Windows:** `~/hexagon/`

**Stored data:**
- Command aliases
- Replay history
- User settings
- CLI installations

**Environment variable:**
```bash
export HEXAGON_CONFIG_STORAGE_PATH=/custom/path
```

### Keyboard Options

#### keymap

Custom keyboard shortcut mappings.

**Type:** `object`
**Default:** `{}`

```yaml
options:
  keymap:
    create_dir: "c-p"  # Ctrl+P for creating directories
    toggle_all: "c-a"  # Ctrl+A for toggling all
```

**Format:**
- `c-<key>`: Control + key
- `m-<key>` or `alt-<key>`: Alt + key
- `s-<key>`: Shift + key

**Available mappings:** (varies by prompt type)

**Environment variable:** Not supported (use YAML only)

## Configuration Examples

### Minimal CI/CD Setup

```yaml
cli:
  name: CI CLI
  command: ci
  options:
    theme: disabled              # No styling for logs
    update_disabled: true        # Don't check for updates in CI
    cli_update_disabled: true
    hints_disabled: true         # No hints needed
    send_telemetry: false       # No telemetry in CI
```

### Development Environment

```yaml
cli:
  name: Dev CLI
  command: dev
  options:
    theme: default               # Full rich output
    update_disabled: false       # Check for updates
    hints_disabled: false        # Show helpful hints
    update_time_between_checks: 3600  # Check hourly
```

### Production Environment

```yaml
cli:
  name: Prod CLI
  command: prod
  options:
    theme: result_only           # Only show results
    update_disabled: false
    hints_disabled: true         # No hints in production
    cwd_tools_disabled: true     # Consistent tools only
```

### Custom Storage Location

```yaml
cli:
  name: My CLI
  command: mycli
  options:
    config_storage_path: /opt/mycli/storage
    # All user data stored in custom location
```

## Option Validation

Hexagon validates options at startup. Invalid options will cause an error:

```yaml
options:
  theme: invalid-theme  # Error: Invalid theme value
```

**Valid themes:** `default`, `disabled`, `result_only`

## Debugging Options

To see which options are active:

```python
# In a plugin or custom tool
from hexagon.runtime.singletons import options

def main():
    print(f"Theme: {options.theme}")
    print(f"Updates disabled: {options.update_disabled}")
```

## Option Storage Locations

Some options are persisted in user storage:

```
~/.config/hexagon/hexagon/
├── options.json         # Persisted option values
├── last-command.txt     # Replay history
└── installations/       # CLI installations
```

## See Also

- [CLI API](cli) - CLI configuration reference
- [Configuration Guide](../getting-started/configuration) - Complete YAML guide
- [Built-in Tools](built-in-tools) - Tools affected by options
- [Theming Guide](../guides/theming) - UI theme details

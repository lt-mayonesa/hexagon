---
sidebar_position: 5
---

# Built-in Tools API

Hexagon provides built-in tools that are automatically available in different contexts. This page documents all built-in tools and when they're available.

## Tool Availability

Hexagon provides tools in two contexts:

### Initial Setup Tools

When you run `hexagon` **without** an `app.yaml` configuration file, these tools are available:

| Tool | Alias | Description |
|------|-------|-------------|
| `install` | - | Install a CLI from YAML configuration |
| `get-json-schema` | - | Get JSON schema for YAML validation |
| `update-hexagon` | - | Update Hexagon framework to latest version |

These tools help you get started with Hexagon or manage the framework itself.

### Default Tools

When you have an `app.yaml` configuration file (CLI project mode), these additional tools are **always** available:

| Tool | Alias | Description |
|------|-------|-------------|
| `save-alias` | - | Save command aliases for quick access |
| `replay` | `r` | Re-run the last executed command |
| `create-tool` | - | Interactive wizard to create new tools |
| `update-cli` | - | Update CLI from git repository |

These tools enhance your CLI workflow and make it easier to maintain your CLI.

## Initial Setup Tools

### install

Installs a CLI from a YAML configuration file.

**Usage:**
```bash
hexagon
# Select "install" from the menu
# Choose your configuration file (app.yaml)
```

**What it does:**
1. Reads your `app.yaml` configuration
2. Creates a command alias for your CLI
3. Makes your CLI available system-wide

**Configuration:**
```yaml
# app.yaml
cli:
  name: My CLI
  command: mycli  # The command you'll use to run your CLI
```

After installation, you can run `mycli` from anywhere to access your CLI.

### get-json-schema

Generates a JSON schema for validating Hexagon YAML configurations.

**Usage:**
```bash
hexagon
# Select "get-json-schema"
```

**What it does:**
- Outputs the complete JSON schema for Hexagon configuration files
- Useful for IDE validation and autocomplete
- Helps catch configuration errors before runtime

**Use with VS Code:**
Add to your `app.yaml`:
```yaml
# yaml-language-server: $schema=<schema-url>

cli:
  name: My CLI
  # ... rest of config
```

### update-hexagon

Updates Hexagon framework to the latest version.

**Usage:**
```bash
hexagon
# Select "update-hexagon"
```

**What it does:**
1. Checks for new Hexagon versions
2. Downloads and installs the latest version
3. Shows changelog with new features and fixes

**Automatic Updates:**
Hexagon also checks for updates automatically (configurable):
```yaml
cli:
  options:
    update_disabled: false  # Enable/disable update checks
    update_time_between_checks: 86400  # Check every 24 hours
```

## Default Tools (CLI Project Mode)

### save-alias

Saves command aliases for frequently used tool and environment combinations.

**Usage:**
```bash
mycli save-alias
```

**What it does:**
- Prompts you to select a tool and environment
- Creates a short alias for that combination
- Saves the alias for future use

**Example:**
```bash
$ mycli save-alias
# Select tool: deploy
# Select environment: production
# Enter alias: dp

$ mycli dp  # Now you can use the alias instead of "mycli deploy production"
```

**Stored location:** `~/.config/hexagon/<cli-name>/aliases.yaml`

### replay (alias: r)

Re-runs the last executed command with the same arguments.

**Usage:**
```bash
mycli replay
# or
mycli r
```

**What it does:**
1. Loads the last command from history
2. Re-executes with the same tool, environment, and arguments
3. Useful for iterative workflows

**Example workflow:**
```bash
$ mycli deploy dev
# ... deployment runs ...

$ mycli r  # Runs "mycli deploy dev" again
```

**Disabling replay:**
To prevent a tool from being recorded in history:
```yaml
tools:
  - name: secret-operation
    action: ./sensitive.sh
    traced: false  # This tool won't be saved in replay history
```

**Stored location:** `~/.config/hexagon/hexagon/last-command.txt`

### create-tool

Interactive wizard for creating new tools in your CLI.

**Usage:**
```bash
mycli create-tool
```

**What it does:**
1. Prompts for tool details (name, type, description)
2. Generates the appropriate configuration
3. Adds the tool to your `app.yaml`
4. Optionally creates template files for custom Python tools

**Supported tool types:**
- Web tools (opens URLs)
- Shell tools (executes commands)
- Custom Python tools (with template generation)
- Tool groups

**Example workflow:**
```bash
$ mycli create-tool
Tool type: shell
Tool name: backup-db
Description: Backup the database
Action: ./scripts/backup.sh
Environment-specific: yes
  dev: backup-dev
  prod: backup-prod

Tool added to app.yaml!
```

### update-cli

Updates your CLI from its git repository.

**Usage:**
```bash
mycli update-cli
```

**What it does:**
1. Checks if your CLI is in a git repository
2. Pulls the latest changes from the remote
3. Reloads the configuration

**Requirements:**
- Your CLI must be in a git repository
- You must have committed your changes
- Remote repository must be accessible

**Configuration:**
```yaml
cli:
  options:
    cli_update_disabled: false  # Enable/disable CLI update checks
```

**Automatic checks:**
Hexagon checks for CLI updates automatically when you run your CLI.

## Disabling Built-in Tools

You cannot disable initial setup tools. However, you can disable certain default tool features:

**Disable update checks:**
```yaml
cli:
  options:
    update_disabled: true        # No Hexagon framework updates
    cli_update_disabled: true    # No CLI project updates
```

**Disable tracing (affects replay):**
```yaml
tools:
  - name: sensitive-tool
    traced: false  # This tool won't be saved for replay
```

## Storage Locations

Built-in tools store data in these locations:

| Data | Location (Linux/macOS) | Location (Windows) |
|------|------------------------|-------------------|
| Aliases | `~/.config/hexagon/<cli>/aliases.yaml` | `~/hexagon/<cli>/aliases.yaml` |
| Replay history | `~/.config/hexagon/hexagon/last-command.txt` | `~/hexagon/hexagon/last-command.txt` |
| User settings | `~/.config/hexagon/hexagon/` | `~/hexagon/hexagon/` |
| CLI installations | `~/.config/hexagon/installations/` | `~/hexagon/installations/` |

Override with:
```yaml
cli:
  options:
    config_storage_path: /custom/path
```

Or environment variable:
```bash
export HEXAGON_STORAGE_PATH=/custom/path
```

## See Also

- [Tool Types Guide](../guides/tool-types) - Overview of all tool types
- [Configuration Guide](../getting-started/configuration) - YAML configuration reference
- [Runtime Options](runtime-options) - Configuring Hexagon behavior
- [Storage API](support/storage) - Working with user data storage

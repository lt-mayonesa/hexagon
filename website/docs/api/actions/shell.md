---
sidebar_position: 2
---

# Shell Actions API

Shell actions execute shell commands, scripts, or Python modules. This page documents how shell actions work and how to configure them in your CLI.

## Overview

Shell actions are the most versatile action type in Hexagon. They can:
- Execute inline shell commands
- Run script files (.sh, .js, etc.)
- Execute Python modules
- Use format string interpolation for dynamic values
- Pass environment-specific configurations

## Action Types

### Inline Commands

Execute shell commands directly:

```yaml
- name: status
  type: shell
  action: git status
```

### Script Files

Execute script files with automatic interpreter detection:

```yaml
- name: deploy
  type: shell
  action: ./scripts/deploy.sh
```

**Supported script types:**

| Extension | Interpreter | Execution |
|-----------|-------------|-----------|
| `.sh` | `sh` | `sh ./scripts/deploy.sh` |
| `.js` | `node` | `node ./scripts/build.js` |

Script paths are relative to your project directory (where your config file is located).

### Python Modules

Reference Python modules that will be imported and executed:

```yaml
- name: analyze
  type: shell
  action: data_analyzer  # Looks for custom_tools/data_analyzer.py
```

Hexagon searches for Python modules in this order:
1. Your `custom_tools_dir`
2. `hexagon.actions.external`

See the [Custom Tools](../../advanced/custom-tools) documentation for details.

## Multiple Commands

Execute a sequence of commands:

```yaml
- name: setup
  type: shell
  action:
    - "echo 'Setting up project...'"
    - "npm install"
    - "npm run build"
    - "echo 'Setup complete!'"
```

Commands are joined with newlines and executed sequentially.

## Format String Interpolation

Inline commands support format strings for dynamic values:

```yaml
- name: deploy
  type: shell
  action: "echo Deploying {tool.name} to {env.name} at {env_args}"
  envs:
    dev: "http://localhost:3000"
    prod: "https://prod.example.com"
```

**Available format variables:**
- `{tool.name}` - Tool name
- `{tool.alias}` - Tool alias
- `{tool.type}` - Tool type
- `{tool.action}` - Tool action
- `{env.name}` - Environment name
- `{env.alias}` - Environment alias
- `{env_args}` - Environment-specific value
- `{cli_args}` - Extra command-line arguments

**Example:**
```bash
$ mycli deploy prod
# Executes: echo Deploying deploy to prod at https://prod.example.com
```

## Environment-Specific Actions

Use the `envs` property for environment-specific commands or configurations:

```yaml
- name: deploy
  type: shell
  envs:
    dev: "echo 'Deploying to dev...' && ./scripts/deploy.sh dev"
    staging: "echo 'Deploying to staging...' && ./scripts/deploy.sh staging"
    prod: "echo 'Deploying to prod...' && ./scripts/deploy.sh prod"
```

When using Python modules, `env_args` can be any type (string, list, dict):

```yaml
- name: configure
  type: shell
  action: configurator
  envs:
    dev:
      host: localhost
      port: 3000
      debug: true
    prod:
      host: prod.example.com
      port: 443
      debug: false
```

## Environment Variables for Scripts

When executing shell scripts, Hexagon automatically sets environment variables:

### HEXAGON_EXECUTION_TOOL

Contains the tool configuration as JSON:

```bash
#!/bin/bash
# scripts/my-script.sh

# Parse tool information
TOOL_NAME=$(echo $HEXAGON_EXECUTION_TOOL | jq -r '.name')
TOOL_TYPE=$(echo $HEXAGON_EXECUTION_TOOL | jq -r '.type')

echo "Executing tool: $TOOL_NAME (type: $TOOL_TYPE)"
```

**Available fields:**
- `name` - Tool name
- `alias` - Tool alias
- `type` - Tool type
- `action` - Tool action
- `description` - Tool description
- `envs` - Environment configurations

### HEXAGON_EXECUTION_ENV

Contains the selected environment configuration as JSON:

```bash
#!/bin/bash
# scripts/deploy.sh

# Parse environment information
ENV_NAME=$(echo $HEXAGON_EXECUTION_ENV | jq -r '.name')
ENV_ALIAS=$(echo $HEXAGON_EXECUTION_ENV | jq -r '.alias')

echo "Deploying to environment: $ENV_NAME ($ENV_ALIAS)"
```

**Available fields:**
- `name` - Environment name
- `alias` - Environment alias
- `long_name` - Long environment name
- `description` - Environment description

### Example: Complete Script

```bash
#!/bin/bash
# scripts/deploy.sh

set -e  # Exit on error

# Get tool and environment info
TOOL_NAME=$(echo $HEXAGON_EXECUTION_TOOL | jq -r '.name')
ENV_NAME=$(echo $HEXAGON_EXECUTION_ENV | jq -r '.name')

echo "======================================="
echo "Tool: $TOOL_NAME"
echo "Environment: $ENV_NAME"
echo "======================================="

# Get environment-specific arguments passed via command line
echo "Arguments: $@"

# Your deployment logic here
./build.sh
./run-tests.sh
./deploy-to-${ENV_NAME}.sh
```

## Passing Arguments to Scripts

Arguments are passed to scripts in order:

1. **Environment arguments** (`env_args` from YAML)
2. **CLI arguments** (extra arguments from command line)

**YAML Configuration:**
```yaml
- name: backup
  type: shell
  action: ./scripts/backup.sh
  envs:
    dev:
      - /data/dev
      - dev-backup
    prod:
      - /data/prod
      - prod-backup
```

**Execution:**
```bash
$ mycli backup dev --full
# Scripts receives:
# $1 = /data/dev
# $2 = dev-backup
# $3 = --full
```

**Script:**
```bash
#!/bin/bash
DATA_DIR=$1
BACKUP_NAME=$2
FULL_FLAG=$3

echo "Backing up $DATA_DIR to $BACKUP_NAME"
if [[ "$FULL_FLAG" == "--full" ]]; then
    echo "Performing full backup"
fi
```

## Action Resolution Order

When you specify an `action`, Hexagon tries to resolve it in this order:

1. **Check if it's a script file** (has `.sh`, `.js` extension)
   - Execute with appropriate interpreter
2. **Try to import as Python module**
   - Check `custom_tools_dir` first
   - Then check `hexagon.actions.external`
3. **Execute as inline shell command**
   - Apply format string interpolation
   - Execute with shell

This allows maximum flexibility in how you define actions.

## Examples

### Inline Command

```yaml
- name: status
  type: shell
  action: git status
```

### Shell Script

```yaml
- name: deploy
  type: shell
  action: ./scripts/deploy.sh
  envs:
    dev: "dev-config"
    prod: "prod-config"
```

### Node.js Script

```yaml
- name: build
  type: shell
  action: ./scripts/build.js
```

### Python Module

```yaml
- name: analyze
  type: shell
  action: data_analyzer
```

### Format String Command

```yaml
- name: open
  type: shell
  action: "open {env_args}"
  envs:
    docs: "https://docs.example.com"
    dashboard: "https://dashboard.example.com"
```

### Multiple Commands

```yaml
- name: setup
  type: shell
  action:
    - "echo 'Installing dependencies...'"
    - "npm install"
    - "echo 'Building project...'"
    - "npm run build"
    - "echo 'Setup complete!'"
```

## Best Practices

### Script Organization
- **Keep scripts in a dedicated directory** (e.g., `scripts/`)
- **Make scripts executable**: `chmod +x scripts/*.sh`
- **Use shebang lines**: `#!/bin/bash` at the top of scripts
- **Handle errors**: Use `set -e` to exit on errors

### Environment Variables
- **Use environment variables for configuration**
- **Access Hexagon context via JSON env vars**
- **Parse JSON with `jq` for complex data**

### Error Handling
- **Return non-zero exit codes on failure**
- **Provide clear error messages**
- **Log important operations**

### Security
- **Validate input arguments**
- **Sanitize file paths**
- **Avoid executing user input directly**

### Flexibility
- **Use `envs` for environment-specific values**
- **Use format strings for dynamic commands**
- **Prefer Python modules for complex logic**

## See Also

- [Tool Types Guide](../../guides/tool-types) - Overview of all tool types
- [Custom Tools](../../advanced/custom-tools) - Creating Python tools
- [Action Execution](../../advanced/action-execution) - How Hexagon resolves and executes actions
- [Configuration Guide](../../getting-started/configuration) - YAML configuration reference

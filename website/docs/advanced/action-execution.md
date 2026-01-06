---
sidebar_position: 5
---

# Action Execution Deep Dive

This guide explains how Hexagon resolves and executes tool actions. Understanding this will help you debug issues and design better tools.

## Overview

When you define a tool with an `action`, Hexagon uses a three-tier strategy to determine how to execute it:

1. **Script File Detection** - Check if it's a file with a known extension
2. **Python Module Import** - Try to import as a Python module
3. **Inline Command Execution** - Execute as a shell command

This flexible approach lets you use different action types without explicitly declaring which type each is.

## Execution Flow Diagram

```
User runs: mycli deploy prod
        ↓
Tool selected: deploy
Environment selected: prod
        ↓
Read action: "./scripts/deploy.sh"
        ↓
┌─────────────────────────────────┐
│ TIER 1: Script File Detection  │
├─────────────────────────────────┤
│ Has file extension? (.sh, .js) │
│ ✓ YES → Execute with interpreter │
│ ✗ NO  → Continue to Tier 2     │
└─────────────────────────────────┘
        ↓
┌─────────────────────────────────┐
│ TIER 2: Python Module Import   │
├─────────────────────────────────┤
│ Try import from custom_tools_dir│
│ Then try hexagon.actions.external│
│ ✓ Found → Call main() function │
│ ✗ Not found → Continue to Tier 3│
└─────────────────────────────────┘
        ↓
┌─────────────────────────────────┐
│ TIER 3: Inline Command         │
├─────────────────────────────────┤
│ Apply format string substitution│
│ Execute with shell              │
└─────────────────────────────────┘
```

## Tier 1: Script File Detection

### How It Works

Hexagon checks if the action has a recognized file extension:

**Supported extensions:**
- `.sh` → executes with `sh`
- `.js` → executes with `node`

**Example:**
```yaml
tools:
  - name: deploy
    action: ./scripts/deploy.sh  # Detected as shell script
```

### Resolution Process

1. Extract file extension from action string
2. If extension matches known type, determine interpreter:
   ```python
   interpreters = {
       ".sh": "sh",
       ".js": "node"
   }
   ```
3. Resolve path relative to project directory
4. Execute: `{interpreter} {script_path} {args}`

### Environment Variables Set

Scripts receive special environment variables:

**HEXAGON_EXECUTION_TOOL** - Tool configuration as JSON:
```bash
#!/bin/bash
TOOL_NAME=$(echo $HEXAGON_EXECUTION_TOOL | jq -r '.name')
echo "Running tool: $TOOL_NAME"
```

**HEXAGON_EXECUTION_ENV** - Environment configuration as JSON:
```bash
ENV_NAME=$(echo $HEXAGON_EXECUTION_ENV | jq -r '.name')
echo "Environment: $ENV_NAME"
```

### Argument Passing

Arguments are passed to scripts in order:

1. **env_args** (from `tool.envs[env.name]`)
2. **cli_args** (extra command-line arguments)

**Example:**
```yaml
tools:
  - name: backup
    action: ./scripts/backup.sh
    envs:
      dev: /data/dev
      prod: /data/prod
```

```bash
$ mycli backup dev --full
# Script receives:
# $1 = /data/dev  (env_args)
# $2 = --full     (cli_args)
```

## Tier 2: Python Module Import

### How It Works

If no file extension is detected, Hexagon tries to import the action as a Python module.

**Search order:**
1. `{custom_tools_dir}/{action}.py`
2. `hexagon.actions.external.{action}`

**Example:**
```yaml
cli:
  custom_tools_dir: ./custom_tools

tools:
  - name: analyze
    action: data_analyzer  # Looks for custom_tools/data_analyzer.py
```

### Module Requirements

The module must have a `main()` function:

```python
# custom_tools/data_analyzer.py

def main(tool, env, env_args, cli_args):
    """
    Main entry point for the tool.

    Args:
        tool: ActionTool object from YAML
        env: Selected Env object (or None)
        env_args: Value from tool.envs[env.name]
        cli_args: Parsed CLI arguments
    """
    # Your code here
    return ["Analysis complete"]
```

### Optional Args Class

Modules can define an `Args` class for custom argument parsing:

```python
from hexagon.support.input.args import ToolArgs, PositionalArg, Arg

class Args(ToolArgs):
    file_path: PositionalArg[str] = Arg(
        None,
        prompt_message="Enter file path"
    )

def main(tool, env, env_args, cli_args: Args):
    # cli_args is now typed as Args
    file_path = cli_args.file_path.value
    # ...
```

### Module Discovery

**Location 1: custom_tools_dir**
```
project/
├── app.yaml
└── custom_tools/
    ├── data_analyzer.py      # Found!
    └── report_generator.py
```

**Location 2: Built-in actions**
```python
# Hexagon looks in hexagon/actions/external/
hexagon.actions.external.open_link  # Built-in action
```

### Import Failure Handling

If import fails, Hexagon continues to Tier 3 (inline command).

**Debug import issues:**
```python
# Add to your custom tool
print("Module loaded successfully!")

def main(tool, env, env_args, cli_args):
    print(f"Executing {tool.name}")
```

## Tier 3: Inline Command Execution

### How It Works

If the action isn't a script file or Python module, it's executed as a shell command.

**Example:**
```yaml
tools:
  - name: status
    action: git status  # Executed as shell command
```

### Format String Substitution

Inline commands support format strings for dynamic values:

**Available variables:**
- `{tool.name}` - Tool name
- `{tool.alias}` - Tool alias
- `{tool.type}` - Tool type
- `{tool.action}` - Tool action string
- `{env.name}` - Environment name
- `{env.alias}` - Environment alias
- `{env_args}` - Environment-specific value
- `{cli_args}` - Extra CLI arguments (space-separated)

**Example:**
```yaml
tools:
  - name: deploy
    action: "echo Deploying {tool.name} to {env.name} at {env_args}"
    envs:
      dev: "localhost:3000"
      prod: "prod.example.com"
```

```bash
$ mycli deploy prod
# Executes: echo Deploying deploy to prod at prod.example.com
```

### Multiple Commands

Actions can be lists of commands:

```yaml
tools:
  - name: setup
    action:
      - "echo 'Step 1: Install dependencies'"
      - "npm install"
      - "echo 'Step 2: Build project'"
      - "npm run build"
```

Commands are joined with newlines and executed as a single script:
```bash
echo 'Step 1: Install dependencies'
npm install
echo 'Step 2: Build project'
npm run build
```

### Shell Execution

Commands are executed with:
```python
subprocess.run(command, shell=True)
```

This means you have access to:
- Shell features (pipes, redirects, etc.)
- Environment variables
- Current working directory

## Environment-Specific Actions

The `envs` property can contain different action types per environment:

```yaml
tools:
  - name: deploy
    envs:
      dev: "./scripts/deploy-dev.sh"     # Script file
      staging: deploy_staging             # Python module
      prod: "kubectl apply -f prod.yaml"  # Inline command
```

Each environment's value goes through the same three-tier resolution.

## Action Resolution Examples

### Example 1: Script File

```yaml
tools:
  - name: backup
    action: ./scripts/backup.sh
```

**Resolution:**
1. **Tier 1**: Has `.sh` extension → Script file detected ✓
2. Execute: `sh ./scripts/backup.sh`

### Example 2: Python Module (Custom)

```yaml
cli:
  custom_tools_dir: ./tools

tools:
  - name: process
    action: data_processor
```

**Resolution:**
1. **Tier 1**: No file extension → Continue
2. **Tier 2**: Try import `./tools/data_processor.py` → Found ✓
3. Execute: `data_processor.main(tool, env, env_args, cli_args)`

### Example 3: Python Module (Built-in)

```yaml
tools:
  - name: docs
    type: web
    action: open_link
```

**Resolution:**
1. **Tier 1**: No file extension → Continue
2. **Tier 2**: Try import `custom_tools/open_link.py` → Not found
3. **Tier 2**: Try import `hexagon.actions.external.open_link` → Found ✓
4. Execute: `open_link.main(tool, env, env_args, cli_args)`

### Example 4: Inline Command

```yaml
tools:
  - name: status
    action: git status --short
```

**Resolution:**
1. **Tier 1**: No file extension → Continue
2. **Tier 2**: Try import `git` → Not found (ModuleNotFoundError)
3. **Tier 3**: Execute as inline command ✓
4. Execute: `git status --short`

### Example 5: Format String

```yaml
tools:
  - name: open
    action: "open {env_args}"
    envs:
      docs: https://docs.example.com
      dashboard: https://dashboard.example.com
```

**Resolution:**
1. **Tier 1**: No file extension → Continue
2. **Tier 2**: Try import `open {env_args}` → Not found
3. **Tier 3**: Execute as inline command ✓
4. Apply format substitution: `open https://docs.example.com`
5. Execute: `open https://docs.example.com`

## Debugging Action Resolution

### Add Debug Output

```yaml
tools:
  - name: test
    action: "echo 'Action: {tool.action}' && echo 'Args: {env_args}'"
```

### Check Module Import

```python
# Test import manually
import sys
sys.path.append("./custom_tools")

try:
    import my_module
    print("Module found!")
    print(dir(my_module))  # Check if 'main' exists
except ModuleNotFoundError:
    print("Module not found!")
```

### Verify Script Path

```bash
# Check if script exists
ls -la scripts/deploy.sh

# Check if executable
file scripts/deploy.sh

# Test script directly
sh scripts/deploy.sh
```

### Enable Python Verbosity

```bash
python -v -m hexagon
# Shows all module imports
```

## Best Practices

### Choose the Right Action Type

| Scenario | Best Type | Why |
|----------|-----------|-----|
| Simple commands | Inline | Quick, no extra files |
| Complex shell logic | Script file | Better error handling, reusable |
| Python logic | Python module | Full language features, testable |
| Dynamic commands | Format string | Environment-specific, flexible |

### Naming Conventions

- **Scripts**: Use descriptive names (`deploy-production.sh`, not `dp.sh`)
- **Python modules**: Use Python naming (`data_processor`, not `data-processor`)
- **Commands**: Use full command names for clarity

### Error Handling

**In scripts:**
```bash
#!/bin/bash
set -e  # Exit on first error
set -u  # Exit on undefined variable

# Your script code
```

**In Python modules:**
```python
from hexagon.domain.hexagon_error import HexagonError

def main(tool, env, env_args, cli_args):
    try:
        # Your code
        return ["Success"]
    except Exception as e:
        raise HexagonError(f"Operation failed: {e}")
```

### Path Management

Always use paths relative to the config file:

```yaml
cli:
  custom_tools_dir: ./tools  # Relative to app.yaml

tools:
  - name: deploy
    action: ./scripts/deploy.sh  # Relative to app.yaml
```

## See Also

- [Shell Actions API](../api/actions/shell) - Script execution details
- [Custom Tools](custom-tools) - Python module development
- [Tool Types Guide](../guides/tool-types) - Overview of all tool types
- [Troubleshooting](../guides/troubleshooting) - Debugging action issues

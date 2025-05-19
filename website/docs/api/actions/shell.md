---
sidebar_position: 2
---

# Shell Actions

Shell actions execute shell commands. This page documents how to configure and use shell actions in your CLI.

## Configuration

Shell actions are configured using the `ActionTool` class with `type` set to `shell`:

```yaml
- name: deploy
  alias: dep
  long_name: Deploy Service
  description: Deploy the service
  type: shell
  action: ./scripts/deploy.sh
```

## Single vs. Multiple Commands

Shell actions can be a single command or multiple commands:

### Single Command

```yaml
action: ./scripts/deploy.sh
```

### Multiple Commands

```yaml
action:
  - "echo 'Starting deployment...'" 
  - "cd /path/to/project"
  - "./scripts/deploy.sh"
```

When multiple commands are specified, they are joined with newlines and executed as a single script.

## Environment-Specific Commands

Shell actions can have different commands for different environments using the `envs` property:

```yaml
- name: deploy
  alias: dep
  long_name: Deploy Service
  description: Deploy the service
  type: shell
  envs:
    dev: "echo 'Deploying to development...' && ./scripts/deploy-dev.sh"
    staging: "echo 'Deploying to staging...' && ./scripts/deploy-staging.sh"
    prod: "echo 'Deploying to production...' && ./scripts/deploy-prod.sh"
```

When the tool is executed, Hexagon will use the command for the selected environment.

## Command Parameters

You can include parameters in your commands:

```yaml
- name: greet
  alias: g
  long_name: Greet
  description: Greet someone
  type: shell
  action: echo "Hello, {name}!"
```

When the tool is executed, Hexagon will prompt the user for the parameter values.

## Implementation

Internally, shell actions are implemented in the `hexagon/actions/shell.py` module. The shell command is executed using the `subprocess` module:

```python
def execute_shell_command(command):
    """Execute a shell command and return the output."""
    import subprocess
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.splitlines()
    else:
        return [f"Error: {result.stderr}"]
```

## Examples

### Simple Shell Tool

```yaml
- name: deploy
  alias: dep
  long_name: Deploy Service
  description: Deploy the service
  type: shell
  action: ./scripts/deploy.sh
```

### Shell Tool with Multiple Commands

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

### Shell Tool with Parameters

```yaml
- name: greet
  alias: g
  long_name: Greet
  description: Greet someone
  type: shell
  action: echo "Hello, {name}!"
```

### Shell Tool with Environment-Specific Commands

```yaml
- name: deploy
  alias: dep
  long_name: Deploy Service
  description: Deploy the service
  type: shell
  envs:
    dev: "echo 'Deploying to development...' && ./scripts/deploy-dev.sh"
    staging: "echo 'Deploying to staging...' && ./scripts/deploy-staging.sh"
    prod: "echo 'Deploying to production...' && ./scripts/deploy-prod.sh"
```

## Best Practices

- **Use Scripts for Complex Commands**: For complex operations, create a script and call it from your shell tool
- **Handle Errors**: Make sure your commands handle errors gracefully
- **Use Environment-Specific Commands**: Configure different commands for different environments
- **Use Parameters**: Use parameters to make your shell tools more flexible
- **Provide Clear Descriptions**: Make it clear what the shell tool does
- **Use Consistent Naming**: Use consistent naming conventions for shell tools

---
sidebar_position: 6
---

# Troubleshooting

This guide covers common issues you might encounter when using Hexagon and how to resolve them.

## Installation Issues

### Command not found after installation

**Problem:** After running `hexagon` and installing your CLI, the command is not found.

**Solutions:**

1. **Restart your terminal** - The shell needs to reload PATH
   ```bash
   # Close and reopen your terminal, or:
   source ~/.bashrc  # or ~/.zshrc
   ```

2. **Check installation location**
   ```bash
   which hexagon
   # Should show the hexagon installation path
   ```

3. **Verify Python/pipx installation**
   ```bash
   pip show hexagon
   # or
   pipx list | grep hexagon
   ```

### Permission denied when installing

**Problem:** `PermissionError` when trying to install Hexagon or a CLI.

**Solutions:**

1. **Use pipx instead of pip** (recommended)
   ```bash
   pipx install hexagon
   ```

2. **Use user installation with pip**
   ```bash
   pip install --user hexagon
   ```

3. **Use virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install hexagon
   ```

## Configuration Issues

### YAML parsing errors

**Problem:** `YAML parse error` or `Invalid configuration` messages.

**Solutions:**

1. **Check YAML syntax**
   - Ensure proper indentation (use spaces, not tabs)
   - Verify colons have spaces after them: `name: value`
   - Check for special characters that need quoting

2. **Validate with JSON schema**
   ```bash
   hexagon get-json-schema > schema.json
   # Use IDE validation or online YAML validators
   ```

3. **Common YAML mistakes:**
   ```yaml
   # Wrong - no space after colon
   name:value

   # Correct
   name: value

   # Wrong - tabs instead of spaces
   →tools:

   # Correct - use spaces
     tools:
   ```

### Config file not found

**Problem:** `Configuration file not found` error.

**Solutions:**

1. **Check file name** - Hexagon looks for `app.yaml` or `app.yml`

2. **Set HEXAGON_CONFIG_FILE environment variable**
   ```bash
   export HEXAGON_CONFIG_FILE=/path/to/your/config.yaml
   mycli
   ```

3. **Check current directory**
   ```bash
   ls -la | grep app.yaml
   # Config file should be in the current directory
   ```

## Action Execution Issues

### Tool not found / Action not found

**Problem:** `Tool not found` or `ModuleNotFoundError` when executing a tool.

**Solutions:**

1. **For Python modules:**
   ```yaml
   cli:
     custom_tools_dir: ./custom_tools  # Ensure this is set

   tools:
     - name: my-tool
       action: my_module  # Should be in custom_tools/my_module.py
   ```

2. **For script files:**
   ```yaml
   tools:
     - name: deploy
       action: ./scripts/deploy.sh  # Path relative to config file
   ```

3. **Check file exists**
   ```bash
   ls -la scripts/deploy.sh
   # Verify file exists at the path specified
   ```

4. **Debug action resolution:**
   - Add print statements to see what's being executed
   - Check if it's a script, module, or inline command
   - See [Action Execution](../advanced/action-execution) for resolution order

### Module import errors

**Problem:** `ModuleNotFoundError` or `ImportError` for custom Python tools.

**Solutions:**

1. **Verify custom_tools_dir is set:**
   ```yaml
   cli:
     custom_tools_dir: ./custom_tools
   ```

2. **Check module structure:**
   ```
   custom_tools/
   ├── __init__.py  # Not required but good practice
   └── my_tool.py   # Your tool module
   ```

3. **Ensure main() function exists:**
   ```python
   # custom_tools/my_tool.py
   def main(tool, env, env_args, cli_args):
       # Your code here
       pass
   ```

4. **Check Python path:**
   ```python
   import sys
   print(sys.path)  # custom_tools_dir should be in this list
   ```

### Script permission denied

**Problem:** `Permission denied` when executing a script.

**Solutions:**

1. **Make script executable:**
   ```bash
   chmod +x scripts/deploy.sh
   ```

2. **Check shebang line:**
   ```bash
   #!/bin/bash
   # Should be the first line of your script
   ```

3. **Verify script path:**
   ```bash
   ls -la scripts/deploy.sh
   # Should show -rwxr-xr-x (executable permissions)
   ```

## Environment Issues

### Environment not working / env_args is None

**Problem:** Environment-specific values aren't being used.

**Solutions:**

1. **Check environment name matches exactly:**
   ```yaml
   envs:
     - name: development  # Must match exactly

   tools:
     - name: deploy
       envs:
         development: value  # Same name
   ```

2. **Use wildcard for all environments:**
   ```yaml
   tools:
     - name: open-docs
       envs:
         "*": https://docs.example.com
   ```

3. **Check if tool requires environment:**
   - If no `envs` in tool definition, no environment selection happens
   - Use `envs` only when you need environment-specific values

### Wrong environment selected

**Problem:** Hexagon selects the wrong environment or doesn't prompt.

**Solutions:**

1. **Explicitly specify environment:**
   ```bash
   mycli deploy production  # Specify environment name
   ```

2. **Check environment aliases:**
   ```yaml
   envs:
     - name: production
       alias: prod  # Can use "prod" instead
   ```

3. **Verify tool has envs defined:**
   ```yaml
   tools:
     - name: deploy
       envs:  # Without this, no environment selection
         dev: config-dev
         prod: config-prod
   ```

## Plugin Issues

### Plugin not loading

**Problem:** Plugin code doesn't execute or errors occur.

**Solutions:**

1. **Verify plugin path:**
   ```yaml
   cli:
     plugins:
       - plugins/my_plugin.py  # Path relative to config file
   ```

2. **Check main() function:**
   ```python
   # plugins/my_plugin.py
   def main():  # Must be named 'main', takes no parameters
       print("Plugin loaded!")
   ```

3. **Check for Python errors:**
   - Syntax errors in plugin file
   - Import errors
   - Exception during initialization

4. **Debug plugin loading:**
   ```python
   def main():
       print("Plugin main() called")  # Should see this when CLI starts
       # Rest of plugin code
   ```

### Hook not firing

**Problem:** Registered hooks don't execute.

**Solutions:**

1. **Verify hook subscription:**
   ```python
   from hexagon.support.hooks import HexagonHooks
   from hexagon.support.hooks.hook import HookSubscription

   def main():
       HexagonHooks.start.subscribe(
           HookSubscription("my-hook", callback=my_function)
       )
   ```

2. **Check callback signature:**
   ```python
   # Hooks with data
   def on_tool_selected(selection):  # Takes data parameter
       print(f"Tool: {selection.value.name}")

   # Hooks without data
   def on_start():  # No parameters
       print("Starting")
   ```

3. **Ensure plugin main() is called:**
   - Plugin must be loaded
   - main() must execute without errors

## Argument Issues

### Arguments not prompting

**Problem:** Tool doesn't prompt for arguments.

**Solutions:**

1. **Check Args class exists:**
   ```python
   from hexagon.support.input.args import ToolArgs, PositionalArg, Arg

   class Args(ToolArgs):
       name: PositionalArg[str] = Arg(None, prompt_message="Enter name")
   ```

2. **Verify prompt logic:**
   ```python
   def main(tool, env, env_args, cli_args: Args):
       if not cli_args.name.value:
           cli_args.name.prompt()  # Must explicitly call prompt()
   ```

3. **Check default values:**
   ```python
   # Won't prompt if default is not None
   name: OptionalArg[str] = Arg("default", prompt_message="Name")

   # Will prompt if value is None
   name: PositionalArg[str] = Arg(None, prompt_message="Name")
   ```

### Argument validation errors

**Problem:** `ValidationError` when passing arguments.

**Solutions:**

1. **Check argument type:**
   ```python
   age: PositionalArg[int] = Arg(None)  # Expects integer
   # mycli tool "not-a-number"  # Will fail
   # mycli tool 25  # Will work
   ```

2. **Use proper format:**
   ```bash
   mycli tool arg1 arg2        # Positional args
   mycli tool --flag value     # Optional args
   mycli tool --flag=value     # Alternative format
   ```

3. **Add validation:**
   ```python
   from pydantic import validator

   class Args(ToolArgs):
       email: PositionalArg[str] = Arg(None)

       @validator("email")
       def validate_email(cls, v):
           if "@" not in v:
               raise ValueError("Must be a valid email")
           return v
   ```

## Performance Issues

### Slow CLI startup

**Problem:** CLI takes a long time to start.

**Solutions:**

1. **Reduce plugin count** - Each plugin adds startup time

2. **Lazy load heavy imports:**
   ```python
   def main(tool, env, env_args, cli_args):
       # Import heavy modules only when needed
       import heavy_module
       # Use module
   ```

3. **Disable update checks temporarily:**
   ```yaml
   cli:
     options:
       update_disabled: true
       cli_update_disabled: true
   ```

4. **Profile startup:**
   ```bash
   time mycli  # Measure startup time
   ```

### Slow tool execution

**Problem:** Tool takes a long time to execute.

**Solutions:**

1. **Profile your code:**
   ```python
   import time
   start = time.time()
   # Your code
   print(f"Took {time.time() - start:.2f}s")
   ```

2. **Use background hooks for non-critical tasks:**
   ```python
   from hexagon.support.hooks.hook import HookSubscrptionType

   HexagonHooks.tool_executed.subscribe(
       HookSubscription(
           "telemetry",
           callback=send_telemetry,
           type=HookSubscrptionType.background  # Don't block
       )
   )
   ```

3. **Optimize scripts:**
   - Remove unnecessary operations
   - Cache expensive computations
   - Use parallel execution where possible

## Debugging Tips

### Enable verbose output

```bash
# Run Hexagon with Python's verbose mode
python -v -m hexagon

# Or with debugging
python -m pdb -m hexagon
```

### Check logs

```python
# Add logging to your tools
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main(tool, env, env_args, cli_args):
    logger.debug(f"Tool: {tool.name}")
    logger.debug(f"Env: {env}")
    logger.debug(f"Args: {cli_args}")
```

### Inspect configuration

```python
# In a plugin or tool
from hexagon.runtime.singletons import cli, tools, envs

def main():
    print("CLI:", cli.name)
    print("Tools:", [t.name for t in tools])
    print("Envs:", [e.name for e in envs])
```

### Test tools in isolation

```python
# Test a tool function directly
from custom_tools import my_tool

# Call main() directly
my_tool.main(tool=None, env=None, env_args=None, cli_args=None)
```

## Getting Help

If you're still stuck:

1. **Check GitHub Issues:** https://github.com/lt-mayonesa/hexagon/issues
2. **Read the docs:** Start with [Getting Started](../getting-started/installation)
3. **Review examples:** Check the [hexagon-tools template](https://github.com/lt-mayonesa/hexagon-tools)
4. **Ask for help:** Open a new issue with:
   - Hexagon version (`hexagon --version`)
   - Your configuration file (sanitized)
   - Error messages (full stack trace)
   - Steps to reproduce

## See Also

- [Configuration Guide](../getting-started/configuration)
- [Custom Tools](../advanced/custom-tools)
- [Action Execution](../advanced/action-execution)
- [Plugins Guide](plugins)

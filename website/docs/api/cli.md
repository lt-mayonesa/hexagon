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
| `options` | `Optional[dict]` | Additional options for the CLI | No |

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
| `shell` | `Optional[str]` | Custom shell to use for commands | No |
| `pre_command` | `Optional[str]` | Command to run before each tool execution | No |
| `environ` | `Dict[str, Any]` | Environment variables to set | No |

## Example

Here's an example of a CLI configuration in YAML:

```yaml
cli:
  name: Team CLI
  command: team
  custom_tools_dir: ./custom_tools
  plugins:
    - my_plugin
  entrypoint:
    shell: /bin/bash
    pre_command: source .env
    environ:
      DEBUG: "true"
```

And here's how you might create a `Cli` instance programmatically:

```python
from hexagon.domain.cli import Cli, EntrypointConfig

entrypoint = EntrypointConfig(
    shell="/bin/bash",
    pre_command="source .env",
    environ={"DEBUG": "true"}
)

cli = Cli(
    name="Team CLI",
    command="team",
    entrypoint=entrypoint,
    custom_tools_dir="./custom_tools",
    plugins=["my_plugin"]
)
```

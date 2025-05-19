---
sidebar_position: 3
---

# Environment API

The `Env` class represents environments in your CLI. This page documents the properties and methods of the `Env` class.

## Env Class

The `Env` class is defined in `hexagon/domain/env.py` and uses Pydantic for data validation.

```python
class Env(BaseModel):
    name: str
    alias: Optional[str] = None
    long_name: Optional[str] = None
    description: Optional[str] = None
```

### Properties

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `name` | `str` | The name of the environment | Yes |
| `alias` | `Optional[str]` | Short alias for the environment | No |
| `long_name` | `Optional[str]` | Longer descriptive name | No |
| `description` | `Optional[str]` | Detailed description | No |

## Example

Here's an example of environment configurations in YAML:

```yaml
envs:
  - name: development
    alias: dev
    long_name: Development Environment
    description: Used for local development
  - name: staging
    alias: stg
    long_name: Staging Environment
    description: Used for testing before production
  - name: production
    alias: prod
    long_name: Production Environment
    description: Live production environment
```

And here's how you might create `Env` instances programmatically:

```python
from hexagon.domain.env import Env

dev_env = Env(
    name="development",
    alias="dev",
    long_name="Development Environment",
    description="Used for local development"
)

staging_env = Env(
    name="staging",
    alias="stg",
    long_name="Staging Environment",
    description="Used for testing before production"
)

prod_env = Env(
    name="production",
    alias="prod",
    long_name="Production Environment",
    description="Live production environment"
)

envs = [dev_env, staging_env, prod_env]
```

## Using Environments with Tools

Tools can have environment-specific configurations using the `envs` property:

```python
from hexagon.domain.tool import ActionTool, ToolType

web_tool = ActionTool(
    name="docs",
    alias="d",
    long_name="Documentation",
    description="Open team documentation",
    type=ToolType.web,
    action="open_link",
    envs={
        "development": "https://docs-dev.example.com",
        "staging": "https://docs-staging.example.com",
        "production": "https://docs.example.com"
    }
)
```

When a tool is executed, Hexagon will use the configuration for the selected environment.

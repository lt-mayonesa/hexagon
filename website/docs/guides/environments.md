---
sidebar_position: 3
---

# Environments

Hexagon supports multiple environments, allowing you to configure different settings for different contexts (development, staging, production, etc.). This guide explains how to configure and use environments in your CLI.

## Defining Environments

Environments are defined in the `envs` section of your configuration file:

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

### Environment Properties

| Property | Description | Required |
|----------|-------------|----------|
| `name` | The name of the environment | Yes |
| `alias` | Short alias for the environment | No |
| `long_name` | Longer descriptive name | No |
| `description` | Detailed description | No |

## Environment-Specific Tool Configuration

Many tools need different configurations for different environments. You can specify environment-specific settings using the `envs` property in a tool configuration:

### Web Tool Example

```yaml
- name: docs
  alias: d
  long_name: Documentation
  description: Open team documentation
  type: web
  envs:
    development: https://docs-dev.example.com
    staging: https://docs-staging.example.com
    production: https://docs.example.com
  action: open_link
```

In this example, the `docs` tool will open different URLs depending on the selected environment.

### Shell Tool Example

```yaml
- name: deploy
  alias: dep
  long_name: Deploy Service
  type: shell
  envs:
    development: "echo 'Deploying to development...' && ./scripts/deploy-dev.sh"
    staging: "echo 'Deploying to staging...' && ./scripts/deploy-staging.sh"
    production: "echo 'Deploying to production...' && ./scripts/deploy-prod.sh"
```

In this example, the `deploy` tool will run different shell commands depending on the selected environment.

## Using Environments

When running your CLI, you can specify an environment using the `-e` or `--env` flag:

```bash
mycli tool-name -e development
```

Or using the environment alias:

```bash
mycli tool-name -e dev
```

If no environment is specified, Hexagon will prompt you to select one if the tool has environment-specific configurations.

## Default Environment

You can set a default environment by setting the `HEXAGON_DEFAULT_ENV` environment variable:

```bash
export HEXAGON_DEFAULT_ENV=development
```

This will make Hexagon use the specified environment by default when no environment is explicitly provided.

## Best Practices

- **Consistent Naming**: Use consistent naming conventions for environments
- **Clear Aliases**: Use short, intuitive aliases for frequently used environments
- **Complete Configuration**: Ensure all tools have configurations for all relevant environments
- **Environment Variables**: Use environment variables for sensitive information
- **Documentation**: Document the purpose and usage of each environment

## Next Steps

Learn how to customize the appearance of your CLI with [Theming](theming).

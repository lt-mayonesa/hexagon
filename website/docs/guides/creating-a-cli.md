---
sidebar_position: 1
---

# Creating a CLI

This guide provides a comprehensive walkthrough of creating a custom CLI with Hexagon. We'll cover the entire process from planning to implementation.

## Planning Your CLI

Before creating your CLI, consider the following:

1. **Purpose**: What problem will your CLI solve for your team?
2. **Tools**: What actions will users need to perform?
3. **Environments**: What environments will your team work with?
4. **Organization**: How should tools be organized for easy discovery?

## Creating the Configuration File

Start by creating a YAML configuration file for your CLI. You can use either:

- The [Hexagon template repository](https://github.com/lt-mayonesa/hexagon-tools)
- A new YAML file from scratch

### Basic Structure

Here's a template to get you started:

```yaml
cli:
  name: Team CLI
  command: team
  custom_tools_dir: ./custom_tools  # Optional

envs:
  - name: development
    alias: dev
  - name: staging
    alias: stg
  - name: production
    alias: prod

tools:
  # Your tools will go here
```

## Adding Tools

Tools are the core of your CLI. Here are examples of different tool types:

### Web Tool

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

### Shell Tool

```yaml
- name: deploy
  alias: dep
  long_name: Deploy Service
  description: Deploy the service
  type: shell
  action: ./scripts/deploy.sh
```

### Function Tool

For function tools, you'll need to implement the function in a Python file and place it in your `custom_tools_dir`:

```yaml
- name: analyze
  alias: a
  long_name: Analyze Data
  description: Run data analysis
  type: function
  function: custom_tools.analysis.analyze_data
```

### Tool Group

```yaml
- name: infra
  alias: i
  long_name: Infrastructure
  description: Infrastructure tools
  type: group
  tools:
    - name: provision
      alias: p
      long_name: Provision Resources
      type: shell
      action: ./scripts/provision.sh
    - name: teardown
      alias: t
      long_name: Teardown Resources
      type: shell
      action: ./scripts/teardown.sh
```

## Installing Your CLI

Once your configuration is ready:

1. Run Hexagon:
   ```bash
   hexagon
   ```

2. Select the "Install CLI" option

3. Choose your configuration file

4. Hexagon will install your CLI, making it available as a command

## Testing Your CLI

Test your CLI by running the command you specified:

```bash
team
```

Verify that all tools and environments work as expected.

## Distributing Your CLI

To share your CLI with your team:

1. **Version Control**: Store your configuration in a Git repository

2. **Documentation**: Add a README explaining how to install and use the CLI

3. **Onboarding**: Include CLI installation in your team's onboarding process

## Best Practices

- **Keep it Simple**: Start with a few essential tools and expand as needed
- **Consistent Naming**: Use consistent naming conventions for tools and aliases
- **Documentation**: Document each tool's purpose and usage
- **Maintenance**: Regularly update your CLI as team workflows evolve
- **Feedback**: Collect feedback from your team to improve the CLI

## Next Steps

Learn more about the different [Tool Types](tool-types) you can use in your CLI.

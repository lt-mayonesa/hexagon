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

### Custom Python Tool

For custom Python tools, see the [Custom Tools](../advanced/custom-tools) documentation for details on implementation.

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

## Understanding Action Execution

When you specify an `action` for a tool, Hexagon intelligently resolves how to execute it:

### Action Types

**1. Script Files** (`.sh`, `.js` extensions)
```yaml
action: ./scripts/deploy.sh
```
Hexagon detects the file extension and uses the appropriate interpreter.

**2. Python Modules**
```yaml
action: data_processor  # Looks for custom_tools/data_processor.py
```
Hexagon imports the module and calls its `main(tool, env, env_args, cli_args)` function.

**3. Inline Commands**
```yaml
action: git status
```
Hexagon executes the command directly in a shell.

**4. Format Strings**
```yaml
action: "echo Deploying to {env.name}"
```
Hexagon replaces `{env.name}`, `{tool.name}`, etc. with actual values.

### Resolution Order

Hexagon tries to resolve actions in this order:

1. Check if it's a script file (has file extension)
2. Try to import as Python module (from `custom_tools_dir` or `hexagon.actions.external`)
3. Execute as inline shell command

This means you can seamlessly mix different action types in your CLI without explicitly declaring which type each is.

### When to Use Each Type

| Use Case | Action Type | Example |
|----------|-------------|---------|
| Simple commands | Inline | `git status`, `docker ps` |
| Deployment scripts | Script file | `./scripts/deploy.sh` |
| Complex logic | Python module | `data_analyzer` |
| Dynamic commands | Format string | `curl {env_args}/api/health` |

See the [Action Execution](../advanced/action-execution) guide for complete details.

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

### Start Small, Grow Incrementally
- Begin with 3-5 essential tools
- Add new tools based on team needs
- Don't try to automate everything at once

### Organize Thoughtfully
- **Use groups** for related tools (e.g., database, deployment, monitoring)
- **Add separators** between logical sections
- **Order tools** by frequency of use

### Naming Conventions
- **Tool names**: Lowercase with hyphens (`deploy-service`, not `DeployService`)
- **Aliases**: Short and memorable (1-3 characters)
- **Descriptions**: Clear and concise (what the tool does)

### Environment Strategy
- Define environments early (dev, staging, prod)
- Use consistent environment names across tools
- Consider using environment aliases for faster access (`d`, `s`, `p`)

### Script Organization
- Keep scripts in a dedicated directory (`scripts/`, `tools/`, etc.)
- Make scripts executable: `chmod +x scripts/*.sh`
- Use meaningful script names
- Add comments and documentation to scripts

### Python Tool Development
- Follow the standard `main(tool, env, env_args, cli_args)` signature
- Use the `Args` class for argument parsing
- Leverage `log` for consistent output
- Handle errors gracefully

### Configuration Management
- **Version control**: Store your config in Git
- **File naming**: Use `app.yaml` for the main config
- **Comments**: Add comments explaining complex configurations
- **Validation**: Use `hexagon get-json-schema` to validate your YAML

### Documentation
- Add a README explaining:
  - How to install the CLI
  - What tools are available
  - How to use each tool
  - How to add new tools
- Document environment-specific configurations
- Include examples of common workflows

### Team Adoption
- Include CLI installation in onboarding
- Provide a quick reference card
- Collect feedback regularly
- Update based on team needs

### Maintenance
- Review and update tools quarterly
- Remove unused tools
- Keep scripts up to date with infrastructure changes
- Monitor for updates to Hexagon itself

## Troubleshooting

Common issues and solutions:

**Tool not found**: Check that the action path is correct (relative to config file)

**Module import error**: Ensure `custom_tools_dir` is set correctly in your config

**Script permission denied**: Make scripts executable with `chmod +x`

**Environment not working**: Verify environment name matches exactly in `envs` section

See the [Troubleshooting Guide](../api/troubleshooting) for more help.

## Next Steps

- Learn about [Tool Types](tool-types) for more options
- Explore [Custom Tools](../advanced/custom-tools) for Python development
- Check out [Action Execution](../advanced/action-execution) to understand how Hexagon works
- Read about [Environments](environments) for multi-environment workflows

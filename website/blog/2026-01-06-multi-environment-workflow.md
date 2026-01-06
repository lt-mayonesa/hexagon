---
slug: multi-environment-workflow
title: "Tutorial: Multi-Environment Workflow"
authors: [joaco]
tags: [tutorial, environments, workflow]
---

# Multi-Environment Workflow

This tutorial demonstrates how to build a CLI with multiple environments for a realistic development workflow. You'll learn how to configure tools for different environments and use them effectively.

<!-- truncate -->

## Scenario

You're building a CLI for your team that deploys a web application to three environments:
- **Development** - Local development server
- **Staging** - Testing environment for QA
- **Production** - Live production servers

Each environment has different configurations for:
- API URLs
- Database connections
- Deployment scripts
- Monitoring dashboards

## Step 1: Define Environments

Start by defining your environments in `app.yaml`:

```yaml
cli:
  name: Deploy CLI
  command: deploy-cli
  custom_tools_dir: ./custom_tools

envs:
  - name: development
    alias: dev
    long_name: Development Environment
    description: Local development environment

  - name: staging
    alias: stg
    long_name: Staging Environment
    description: Pre-production testing environment

  - name: production
    alias: prod
    long_name: Production Environment
    description: Live production environment
```

**Key points:**
- `name`: Full environment name (required)
- `alias`: Short form for quick access (recommended)
- `long_name`: Display name in menus
- `description`: Explains the environment's purpose

## Step 2: Add Web Tools with Environment URLs

Let's add tools to open various dashboards specific to each environment:

```yaml
tools:
  - name: dashboard
    alias: dash
    long_name: Application Dashboard
    description: Open the application dashboard
    type: web
    action: open_link
    envs:
      development: http://localhost:3000
      staging: https://staging.myapp.com
      production: https://myapp.com

  - name: api-docs
    alias: api
    long_name: API Documentation
    description: Open API documentation
    type: web
    action: open_link
    envs:
      development: http://localhost:8080/docs
      staging: https://staging-api.myapp.com/docs
      production: https://api.myapp.com/docs

  - name: logs
    alias: l
    long_name: Application Logs
    description: Open log viewer
    type: web
    action: open_link
    envs:
      development: http://localhost:9000
      staging: https://logs.staging.myapp.com
      production: https://logs.myapp.com
```

**Testing:**
```bash
# Open development dashboard
deploy-cli dashboard dev

# Open staging API docs
deploy-cli api-docs staging

# Production logs (will prompt for environment if not specified)
deploy-cli logs
```

## Step 3: Add Environment-Specific Shell Commands

Now let's add deployment tools with different commands per environment:

```yaml
tools:
  - name: deploy
    alias: d
    long_name: Deploy Application
    description: Deploy the application
    type: shell
    envs:
      development: |
        echo "🚀 Deploying to development..."
        npm run build:dev
        docker-compose -f docker-compose.dev.yml up -d
        echo "✅ Development deployment complete!"
      staging: |
        echo "🚀 Deploying to staging..."
        npm run build:staging
        ./scripts/deploy-staging.sh
        echo "✅ Staging deployment complete!"
      production: |
        echo "🚀 Deploying to production..."
        npm run build:prod
        ./scripts/deploy-production.sh --verify
        echo "✅ Production deployment complete!"

  - name: rollback
    alias: rb
    long_name: Rollback Deployment
    description: Rollback to previous version
    type: shell
    envs:
      development: docker-compose -f docker-compose.dev.yml down && git checkout HEAD~1
      staging: ./scripts/rollback.sh staging
      production: ./scripts/rollback.sh production --confirm
```

**Note:** Use `|` for multi-line commands in YAML.

## Step 4: Create Custom Tool with Environment Logic

Let's create a custom tool that behaves differently based on the environment:

```python
# custom_tools/health_check.py
from hexagon.support.output.printer import log
from hexagon.support.input.args import ToolArgs, OptionalArg, Arg
import urllib.request
import json

class Args(ToolArgs):
    verbose: OptionalArg[bool] = Arg(
        False,
        alias="v",
        description="Show detailed health check information"
    )

def main(tool, env, env_args, cli_args: Args):
    """Check application health for the selected environment."""

    # env_args contains the environment-specific configuration
    if not env_args:
        log.error("No configuration for this environment")
        return ["Error: Environment not configured"]

    # Extract configuration
    config = env_args
    api_url = config.get("api_url")
    check_interval = config.get("check_interval", 30)
    critical = config.get("critical", False)

    # Show environment info
    env_name = env.name if env else "unknown"
    log.info(f"Checking health for: {env_name}")

    if critical:
        log.panel(
            "⚠️  This is a CRITICAL environment\nChanges require approval",
            title="Warning"
        )

    # Perform health check
    try:
        health_url = f"{api_url}/health"
        log.info(f"Checking: {health_url}")

        with urllib.request.urlopen(health_url, timeout=5) as response:
            data = json.loads(response.read().decode())

        status = data.get("status", "unknown")

        if status == "healthy":
            log.info("✅ Service is healthy")
            results = [
                f"Status: {status}",
                f"Check interval: {check_interval}s"
            ]

            if cli_args.verbose.value:
                # Show additional details in verbose mode
                results.extend([
                    f"Uptime: {data.get('uptime', 'N/A')}",
                    f"Version: {data.get('version', 'N/A')}",
                    f"Requests: {data.get('total_requests', 'N/A')}"
                ])

            return results
        else:
            log.error(f"❌ Service is {status}")
            return [f"Status: {status}"]

    except urllib.error.URLError as e:
        log.error(f"Failed to reach service: {str(e)}")
        return [f"Error: Cannot connect to {api_url}"]
    except Exception as e:
        log.error(f"Health check failed: {str(e)}")
        return [f"Error: {str(e)}"]
```

Add the tool to your configuration with environment-specific settings:

```yaml
tools:
  - name: health
    alias: h
    long_name: Health Check
    description: Check application health
    type: shell
    action: health_check
    envs:
      development:
        api_url: http://localhost:8080
        check_interval: 10
        critical: false
      staging:
        api_url: https://staging-api.myapp.com
        check_interval: 30
        critical: false
      production:
        api_url: https://api.myapp.com
        check_interval: 60
        critical: true  # Mark production as critical
```

**Usage:**
```bash
# Basic health check
deploy-cli health dev

# Verbose health check
deploy-cli health prod --verbose
```

## Step 5: Use Format Strings for Dynamic Commands

You can use format strings to create dynamic commands based on environment:

```yaml
tools:
  - name: ssh
    alias: s
    long_name: SSH to Server
    description: SSH into environment server
    type: shell
    envs:
      development: echo "Development runs locally (no SSH needed)"
      staging: ssh deploy@staging-{env.name}.myapp.com
      production: ssh deploy@{env_args}
    # For production, env_args could be: prod-server-01.myapp.com

  - name: db-connect
    alias: db
    long_name: Database Connection
    description: Connect to database
    type: shell
    envs:
      development: psql -h localhost -U dev -d myapp_dev
      staging: psql -h {env_args.host} -U {env_args.user} -d myapp_staging
      production: psql -h {env_args.host} -U {env_args.user} -d myapp_prod
```

For complex env_args, use dictionary format:

```yaml
tools:
  - name: db-connect
    type: shell
    envs:
      staging:
        host: staging-db.myapp.com
        user: staging_user
        database: myapp_staging
      production:
        host: prod-db.myapp.com
        user: prod_user
        database: myapp_prod
```

## Step 6: Create Environment-Specific Tool Groups

Organize tools by environment with groups:

```yaml
tools:
  - name: dev-tools
    long_name: Development Tools
    description: Tools for local development
    type: group
    tools:
      - name: start-local
        description: Start local development server
        type: shell
        action: npm run dev

      - name: test
        description: Run tests
        type: shell
        action: npm test

      - name: lint
        description: Run linter
        type: shell
        action: npm run lint

  - name: prod-tools
    long_name: Production Tools
    description: Production management tools
    type: group
    tools:
      - name: deploy
        description: Deploy to production
        type: shell
        action: ./scripts/deploy-production.sh

      - name: monitor
        description: Open monitoring dashboard
        type: web
        action: open_link
        envs:
          "*": https://monitoring.myapp.com

      - name: incidents
        description: View incident reports
        type: web
        action: open_link
        envs:
          "*": https://incidents.myapp.com
```

## Step 7: Set Default Environment

For convenience, set a default environment:

```bash
# In your shell profile (.bashrc, .zshrc, etc.)
export HEXAGON_DEFAULT_ENV=development
```

Now when you run tools without specifying an environment, development will be used by default:

```bash
# Uses development by default
deploy-cli dashboard

# Explicitly use staging
deploy-cli dashboard staging
```

## Step 8: Create Environment Aliases

Save frequently used environment commands as aliases:

```bash
# Run the save-alias tool
deploy-cli save-alias

# Select tool: deploy
# Select environment: production
# Enter alias: dp

# Now you can use the alias
deploy-cli dp  # Runs: deploy-cli deploy production
```

## Best Practices

### 1. Environment Naming

**Good:**
```yaml
envs:
  - name: development
    alias: dev
  - name: staging
    alias: stg
  - name: production
    alias: prod
```

**Avoid:**
```yaml
envs:
  - name: dev  # Too short for main name
  - name: stage  # Inconsistent with "production"
  - name: live  # Unclear what this means
```

### 2. Configuration Management

**Store sensitive data in environment variables:**

```yaml
tools:
  - name: deploy
    type: shell
    action: deploy_tool
    envs:
      production:
        api_key: "${PROD_API_KEY}"  # Reference env variable
        database_url: "${PROD_DB_URL}"
```

**Don't commit secrets to YAML:**
```yaml
# ❌ BAD - secrets in config file
envs:
  production:
    api_key: "sk_live_abc123..."  # Never do this!
```

### 3. Environment-Specific Safety

Add confirmation for critical environments:

```python
def main(tool, env, env_args, cli_args):
    # Check if production
    if env and env.name == "production":
        log.panel(
            "⚠️  You are about to modify PRODUCTION\nThis action cannot be undone",
            title="Warning"
        )
        confirm = input("Type 'CONFIRM' to proceed: ")
        if confirm != "CONFIRM":
            return ["Cancelled"]

    # Proceed with operation
    # ...
```

### 4. Consistent Tool Configuration

Ensure all environments are configured for each tool:

```yaml
# ✅ GOOD - all environments configured
- name: dashboard
  type: web
  action: open_link
  envs:
    development: http://localhost:3000
    staging: https://staging.myapp.com
    production: https://myapp.com

# ❌ BAD - missing staging
- name: dashboard
  type: web
  action: open_link
  envs:
    development: http://localhost:3000
    production: https://myapp.com
    # staging not configured - will fail!
```

### 5. Use Wildcard for Common Values

When all environments use the same value:

```yaml
- name: docs
  type: web
  action: open_link
  envs:
    "*": https://docs.myapp.com  # Same for all environments
```

## Complete Example

Here's a complete `app.yaml` for a multi-environment CLI:

```yaml
cli:
  name: MyApp CLI
  command: myapp
  custom_tools_dir: ./custom_tools

envs:
  - name: development
    alias: dev
    long_name: Development
    description: Local development environment

  - name: staging
    alias: stg
    long_name: Staging
    description: Pre-production testing

  - name: production
    alias: prod
    long_name: Production
    description: Live production environment

tools:
  # Deployment
  - name: deploy
    alias: d
    long_name: Deploy Application
    type: shell
    action: deploy_app
    envs:
      development:
        target: local
        verify: false
      staging:
        target: staging-cluster
        verify: true
      production:
        target: production-cluster
        verify: true
        require_approval: true

  # Monitoring
  - name: dashboard
    alias: dash
    type: web
    action: open_link
    envs:
      development: http://localhost:3000
      staging: https://staging.myapp.com
      production: https://myapp.com

  - name: logs
    alias: l
    type: web
    action: open_link
    envs:
      development: http://localhost:9000
      staging: https://logs.staging.myapp.com
      production: https://logs.myapp.com

  # Health checks
  - name: health
    alias: h
    type: shell
    action: health_check
    envs:
      development:
        api_url: http://localhost:8080
        critical: false
      staging:
        api_url: https://staging-api.myapp.com
        critical: false
      production:
        api_url: https://api.myapp.com
        critical: true

  # Database
  - name: db-backup
    long_name: Database Backup
    type: shell
    envs:
      development: echo "Development DB backed up locally"
      staging: ./scripts/backup-db.sh staging
      production: ./scripts/backup-db.sh production --verify
```

## Troubleshooting

**Problem:** Environment not found

```bash
$ myapp deploy prod
Error: Environment 'prod' not found
```

**Solution:** Check your environment alias matches:
```yaml
envs:
  - name: production
    alias: prod  # This must match the alias you use
```

**Problem:** Tool fails with "No environment configuration"

```bash
$ myapp deploy dev
Error: No configuration for environment 'development'
```

**Solution:** Ensure tool has configuration for all environments:
```yaml
- name: deploy
  envs:
    development: ./deploy-dev.sh
    staging: ./deploy-staging.sh
    production: ./deploy-prod.sh  # Don't forget any!
```

**Problem:** Environment variables not interpolated

```bash
$ myapp ssh prod
# Shows: ssh user@{env_args.host} instead of actual host
```

**Solution:** Format strings only work with inline commands, not in env_args values. Use this pattern instead:

```yaml
- name: ssh
  type: shell
  action: "ssh user@{env_args}"  # Format string in action
  envs:
    production: prod-server-01.myapp.com
```

## Next Steps

- [Custom Tools](/docs/advanced/custom-tools) - Build sophisticated tools
- [Environments Guide](/docs/guides/environments) - Complete environment reference
- [Action Execution](/docs/advanced/action-execution) - Understand action resolution
- [Troubleshooting](/docs/guides/troubleshooting) - Fix common issues

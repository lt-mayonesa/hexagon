---
sidebar_position: 1
---

# Introduction

## What is Hexagon?

Hexagon is a powerful tool that allows you to **make your team's knowledge truly accessible, truly shared, and truly empowering by creating your own CLI**. It provides a framework for building custom command-line interfaces (CLIs) that encapsulate your team's workflows, tools, and knowledge.

![Hexagon CLI Example](https://user-images.githubusercontent.com/11464844/141402773-2fa1e859-cbe7-43a2-87e8-81620307167f.gif)

## Why Hexagon?

Teams often struggle with knowledge sharing and standardizing workflows. Hexagon solves this by allowing you to:

- **Centralize team knowledge** in a single, accessible interface
- **Standardize workflows** across your team
- **Reduce onboarding time** for new team members
- **Improve productivity** by making common tasks easily accessible
- **Customize and extend** your CLI to fit your team's specific needs

## Key Features

### Declarative YAML Configuration
- **Simple setup**: Define your entire CLI in a single YAML file
- **No coding required**: Create powerful CLIs without writing code
- **Easy to maintain**: Configuration is readable and version-controlled

### Flexible Tool Types
- **Web tools**: Open URLs and dashboards
- **Shell tools**: Execute commands and scripts (.sh, .js)
- **Custom Python tools**: Build sophisticated tools with full Python
- **Function tools**: Register Python functions programmatically
- **Tool groups**: Organize related tools together

### Multi-Environment Support
- **Environment-specific configuration**: Different settings per environment
- **Quick environment switching**: Use environment aliases for fast access
- **Format strings**: Dynamic command generation based on environment

### Extensibility
- **Custom tools**: Write Python modules for complex functionality
- **Plugins**: Extend Hexagon with custom plugins
- **Hooks**: React to lifecycle events (start, tool executed, etc.)
- **Runtime options**: Configure behavior via YAML or environment variables

### Rich Terminal Experience
- **Theming**: Choose from default, disabled, or result-only themes
- **Interactive prompts**: Searchable selections with suggestions
- **Argument parsing**: Built-in support for positional and optional arguments
- **Rich output**: Panels, syntax highlighting, and formatted results

### Built-in Tools
- **Command aliases**: Save frequently used commands
- **Replay**: Re-run the last command
- **Create tool wizard**: Interactive tool creation
- **Auto-updates**: Keep Hexagon and your CLI up-to-date

## Quick Example

```yaml
cli:
  custom_tools_dir: .  # relative to this file
  name: Team CLI
  command: team

envs:
  - name: dev
    alias: d
  - name: prod
    alias: p

tools:
  - name: docs
    alias: d
    long_name: Documentation
    description: Open team documentation
    type: web
    envs:
      dev: https://docs-dev.example.com
      prod: https://docs.example.com
    action: open_link

  - name: deploy
    alias: dep
    long_name: Deploy Service
    type: shell
    action: ./scripts/deploy.sh
```

## Getting Started

Ready to create your team's CLI? Here's how to begin:

1. **[Install Hexagon](getting-started/installation)** - Get Hexagon installed on your machine
2. **[Configure Your CLI](getting-started/configuration)** - Create your first `app.yaml`
3. **[Create a CLI](guides/creating-a-cli)** - Build your custom CLI step-by-step

### Learn by Example

- **[Building a Custom Tool](tutorial-extras/building-custom-tool)** - Create a GitHub repository info tool
- **[Multi-Environment Workflow](tutorial-extras/multi-environment-workflow)** - Set up dev, staging, and production environments

### Explore the Documentation

- **[Tool Types Guide](guides/tool-types)** - All available tool types and when to use them
- **[Custom Tools](advanced/custom-tools)** - Write Python tools for complex functionality
- **[Action Execution](advanced/action-execution)** - Understand how Hexagon resolves actions
- **[API Reference](api/cli)** - Complete API documentation
- **[Troubleshooting](guides/troubleshooting)** - Solutions to common issues

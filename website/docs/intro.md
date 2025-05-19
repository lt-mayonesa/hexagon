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

- **Easy Configuration**: Define your CLI using simple YAML files
- **Multiple Tool Types**: Support for web links, shell commands, and custom functions
- **Environment Support**: Configure different environments (dev, qa, prod, etc.)
- **Theming**: Customize the look and feel of your CLI
- **Plugins**: Extend functionality with plugins
- **Internationalization**: Support for multiple languages

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

Ready to create your team's CLI? Check out the [Installation](getting-started/installation) guide to get started!

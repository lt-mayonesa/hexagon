---
sidebar_position: 1
---

# API Reference

This section provides detailed documentation for Hexagon's API components. Hexagon is designed with a modular architecture that makes it easy to create, customize, and extend your team's CLI.

## Core Components

Hexagon's core architecture consists of several key components:

### CLI

The `Cli` class represents your custom CLI configuration. It defines the name, command, and other properties of your CLI.

[Learn more about CLI configuration](api/cli)

### Tool

The `Tool` class and its subclasses represent the tools available in your CLI. Different tool types (web, shell, custom Python tools, etc.) provide different functionality.

[Learn more about Tool configuration](api/tool)

### Environment

The `Env` class represents environments in your CLI. Environments allow you to configure different settings for different contexts (development, staging, production, etc.).

[Learn more about Environment configuration](api/env)

## Actions

Actions define what happens when a tool is executed. Hexagon provides several built-in action types:

- [Web Actions](api/actions/web): Open web links
- [Shell Actions](api/actions/shell): Execute shell commands

## Support

Hexagon includes several support modules to enhance your CLI:

- [Output](api/support/output): Customize the output of your CLI
- [Hooks](api/support/hooks): Add custom behavior at different points in the CLI lifecycle
- [Storage](api/support/storage): Store and retrieve user data

## Extending Hexagon

Hexagon is designed to be extended. You can create custom tools, plugins, and more to enhance your CLI's functionality.

Check out the [Advanced](advanced/custom-tools) section for more information on extending Hexagon.

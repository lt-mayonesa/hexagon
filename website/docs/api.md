---
sidebar_position: 1
---

# API Reference

Complete API documentation for Hexagon. This section provides detailed references for all components, configuration options, and extensibility features.

## Configuration APIs

Core configuration objects that define your CLI structure:

### [CLI Configuration](api/cli)
The root configuration object for your CLI. Defines the CLI name, command, plugins, custom tools directory, and runtime options.

**Key topics:**
- CLI properties (name, command, entrypoint)
- Plugin configuration
- Custom tools directory
- Runtime options

### [Tool Configuration](api/tool)
Defines tools available in your CLI. Supports multiple tool types including ActionTool, GroupTool, and FunctionTool.

**Key topics:**
- Tool types (web, shell, function, group, separator)
- Tool properties (name, alias, description, action)
- Environment-specific configurations
- Tool groups and organization

### [Environment Configuration](api/env)
Defines environments for multi-environment workflows (development, staging, production, etc.).

**Key topics:**
- Environment properties (name, alias, long_name)
- Environment selection
- Environment-specific tool configuration

### [Runtime Options](api/runtime-options)
Configure Hexagon's runtime behavior including themes, updates, and features.

**Key topics:**
- UI options (theme, hints)
- Update options (update checks, time between checks)
- Feature options (CWD tools, telemetry, dependency scanning)
- Storage and keyboard options
- Environment variable configuration

## Built-in Features

### [Built-in Tools](api/built-in-tools)
Documentation for all built-in Hexagon tools available in different contexts.

**Initial Setup Tools** (available when running `hexagon` without config):
- `install` - Install a CLI from YAML configuration
- `get-json-schema` - Get JSON schema for validation
- `update-hexagon` - Update Hexagon framework

**Default Tools** (available in CLI project mode):
- `save-alias` - Save command aliases
- `replay` (alias: `r`) - Re-run last command
- `create-tool` - Interactive tool creation wizard
- `update-cli` - Update CLI from git repository

## Action APIs

How tools execute their actions:

### [Web Actions](api/actions/web)
Open URLs in the default browser. Used for documentation, dashboards, and web-based tools.

**Key topics:**
- URL configuration
- Environment-specific URLs
- open_link action

### [Shell Actions](api/actions/shell)
Execute shell commands and scripts. Supports .sh and .js files, inline commands, and format strings.

**Key topics:**
- Script execution (.sh, .js files)
- Inline command execution
- Format string substitution
- Environment variables (HEXAGON_EXECUTION_TOOL, HEXAGON_EXECUTION_ENV)
- Argument passing

### [Action Execution Deep Dive](advanced/action-execution)
Comprehensive guide to Hexagon's 3-tier action resolution strategy.

**Key topics:**
- Tier 1: Script file detection
- Tier 2: Python module import
- Tier 3: Inline command execution
- Resolution order and debugging
- Best practices

## Support Modules

Utilities and APIs for building rich CLI experiences:

### [Output API](api/support/output)
Display formatted output with colors, panels, syntax highlighting, and more.

**Key topics:**
- log.info(), log.result(), log.error()
- log.panel() - Highlighted panels
- log.example() - Code examples with syntax highlighting
- Theming and formatting

### [Hooks API](api/support/hooks)
React to lifecycle events and extend CLI functionality.

**Available hooks:**
- `HexagonHooks.start` - CLI startup
- `HexagonHooks.tool_selected` - After tool selection
- `HexagonHooks.env_selected` - After environment selection
- `HexagonHooks.before_tool_executed` - Before tool execution
- `HexagonHooks.tool_executed` - After tool execution
- `HexagonHooks.end` - CLI shutdown

**Key topics:**
- Hook subscription with HookSubscription
- Blocking vs background hooks
- Hook data types
- Use cases and examples

### [Storage API](api/support/storage)
Persist user data, settings, and state across CLI runs.

**Key topics:**
- User storage directory
- Reading and writing data
- Storage locations per platform
- Custom storage paths

## Advanced Topics

Deep dives and advanced features:

### [Custom Tools](advanced/custom-tools)
Build sophisticated Python tools with argument parsing, prompts, and rich output.

**Key topics:**
- main(tool, env, env_args, cli_args) signature
- Args class for argument parsing
- PositionalArg and OptionalArg
- Accessing argument values
- Error handling
- Best practices

### [Prompting](advanced/prompting)
Create interactive prompts with validation, suggestions, and custom inputs.

**Key topics:**
- Arg() parameters (prompt_message, prompt_suggestions, searchable)
- Argument types and validation
- Choices vs suggestions
- Skip tracing for sensitive data

### [Plugins](guides/plugins)
Extend Hexagon with custom plugins that run at CLI startup.

**Key topics:**
- Plugin structure (main() function)
- Plugin loading and registration
- Hook subscription from plugins
- Custom tool registration

## Quick Navigation

**Getting started:**
- [Installation](getting-started/installation) - Install Hexagon
- [Configuration Guide](getting-started/configuration) - Create app.yaml
- [Creating a CLI](guides/creating-a-cli) - Build your first CLI

**Tutorials:**
- [Building a Custom Tool](/blog/building-custom-tool) - Create a GitHub info tool
- [Multi-Environment Workflow](/blog/multi-environment-workflow) - Set up dev/staging/prod

**Reference:**
- [Tool Types Guide](guides/tool-types) - All available tool types
- [Environments Guide](guides/environments) - Multi-environment configuration
- [Troubleshooting](guides/troubleshooting) - Common issues and solutions

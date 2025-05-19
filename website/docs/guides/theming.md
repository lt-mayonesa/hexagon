---
sidebar_position: 4
---

# Theming

Hexagon supports customizing the appearance of your CLI through themes. This guide explains how to configure and use themes in your CLI.

## Available Themes

Hexagon currently supports three built-in themes:

1. **default**: A colorful theme with decorations that provides a rich CLI experience
2. **disabled**: A minimal theme with no colors or decorations, useful for environments where ANSI colors aren't supported
3. **result_only**: A theme that only shows the result logs, useful for scripts and automation

## Setting the Theme

You can set the theme using the `HEXAGON_THEME` environment variable:

```bash
HEXAGON_THEME=default mycli
```

### Examples

#### Default Theme

```bash
HEXAGON_THEME=default mycli
```

This provides a colorful interface with decorations and clear visual hierarchy.

#### Disabled Theme

```bash
HEXAGON_THEME=disabled mycli
```

This disables all colors and decorations, providing a plain text interface that works in all terminal environments.

#### Result Only Theme

```bash
HEXAGON_THEME=result_only mycli
```

This theme only shows the result logs, which is useful when you want to use the output in scripts or other automation.

## Theme Configuration in CLI Options

You can also configure the default theme for your CLI in the configuration file:

```yaml
cli:
  name: My CLI
  command: mycli
  options:
    theme: default
```

This sets the default theme for your CLI, but users can still override it using the `HEXAGON_THEME` environment variable.

## Custom Themes

Currently, Hexagon doesn't support creating custom themes directly through the configuration file. However, you can extend the theming system by creating a plugin if you need more customization options.

## Best Practices

- **Default Theme**: Use the default theme for interactive use
- **Disabled Theme**: Use the disabled theme in environments where ANSI colors aren't supported
- **Result Only Theme**: Use the result_only theme when integrating with scripts or automation
- **Documentation**: Document the available themes and how to set them in your CLI's documentation

## Next Steps

Learn how to extend your CLI's functionality with [Plugins](plugins).

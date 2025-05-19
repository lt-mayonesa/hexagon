---
sidebar_position: 2
---

# Quick Start

This guide will help you quickly set up your first CLI with Hexagon. We'll create a simple CLI with a few tools to demonstrate the basic functionality.

## Creating Your First CLI

Hexagon uses YAML configuration files to define your CLI. Let's create a simple one.

1. Create a new file named `my-cli.yaml` with the following content:

```yaml
cli:
  name: My First CLI
  command: mfc

envs:
  - name: dev
    alias: d
  - name: prod
    alias: p

tools:
  - name: google
    alias: g
    long_name: Google Search
    description: Open Google search
    type: web
    action: open_link
    envs:
      dev: https://google.com?q=dev
      prod: https://google.com

  - name: hello
    alias: h
    long_name: Hello World
    description: Print a greeting
    type: shell
    action: echo "Hello, World!"
```

2. Run Hexagon and select the "Install CLI" option:

```bash
hexagon
```

3. When prompted, select your `my-cli.yaml` file.

4. Hexagon will install your CLI and make it available as a command.

## Using Your CLI

Now that your CLI is installed, you can use it by running the command you specified in the configuration:

```bash
mfc
```

This will display your CLI with the tools you defined. You can select a tool using the arrow keys and press Enter to execute it.

### Using Tool Aliases

You can also directly execute a tool using its alias:

```bash
mfc g
```

This will execute the "google" tool directly.

### Specifying Environments

To specify an environment, use the `-e` or `--env` flag:

```bash
mfc g -e dev
```

Or use the environment alias:

```bash
mfc g -e d
```

## Next Steps

Now that you've created your first CLI, you can learn more about configuring it in the [Configuration](configuration) guide.

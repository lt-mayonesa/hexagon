---
sidebar_position: 1
---

# Web Actions

Web actions open URLs in the default browser. This page documents how to configure and use web actions in your CLI.

## Configuration

Web actions are configured using the `ActionTool` class with `type` set to `web` and `action` set to `open_link`:

```yaml
- name: docs
  alias: d
  long_name: Documentation
  description: Open team documentation
  type: web
  action: open_link
  envs:
    dev: https://docs-dev.example.com
    prod: https://docs.example.com
```

## Environment-Specific URLs

Web actions can have different URLs for different environments using the `envs` property:

```yaml
envs:
  dev: https://docs-dev.example.com
  staging: https://docs-staging.example.com
  prod: https://docs.example.com
```

When the tool is executed, Hexagon will use the URL for the selected environment.

## URL Parameters

You can include parameters in your URLs:

```yaml
- name: search
  alias: s
  long_name: Search
  description: Search for something
  type: web
  action: open_link
  envs:
    dev: https://search-dev.example.com?q={query}
    prod: https://search.example.com?q={query}
```

When the tool is executed, Hexagon will prompt the user for the parameter values.

## Implementation

Internally, web actions are implemented in the `hexagon/actions/web.py` module. The `open_link` function uses the `webbrowser` module to open URLs in the default browser:

```python
def open_link(url):
    """Open a URL in the default browser."""
    import webbrowser
    webbrowser.open(url)
    return [f"Opened {url} in browser"]
```

## Examples

### Simple Web Tool

```yaml
- name: docs
  alias: d
  long_name: Documentation
  description: Open team documentation
  type: web
  action: open_link
  envs:
    dev: https://docs-dev.example.com
    prod: https://docs.example.com
```

### Web Tool with Parameters

```yaml
- name: search
  alias: s
  long_name: Search
  description: Search for something
  type: web
  action: open_link
  envs:
    dev: https://search-dev.example.com?q={query}
    prod: https://search.example.com?q={query}
```

### Web Tool with Multiple Parameters

```yaml
- name: jira
  alias: j
  long_name: JIRA Issue
  description: Open a JIRA issue
  type: web
  action: open_link
  envs:
    dev: https://jira-dev.example.com/browse/{project}-{issue}
    prod: https://jira.example.com/browse/{project}-{issue}
```

## Best Practices

- **Use Environment-Specific URLs**: Configure different URLs for different environments
- **Use Parameters**: Use parameters to make your web tools more flexible
- **Provide Clear Descriptions**: Make it clear what the web tool does
- **Use Consistent Naming**: Use consistent naming conventions for web tools

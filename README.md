# hexagon
Make your team's knowledge truly accessible, truly shared, and truly empowering by creating your own CLI.

[![build](https://github.com/redbeestudios/hexagon/actions/workflows/python-package.yml/badge.svg)](https://github.com/redbeestudios/hexagon/actions/workflows/python-package.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![hexagon setup example](https://user-images.githubusercontent.com/11464844/141402773-2fa1e859-cbe7-43a2-87e8-81620307167f.gif)](https://asciinema.org/a/Mk8of7EC0grfsSgWYrEdGCjdF)

---

## Getting Started

### Install hexagon
```bash
python3 -m pip install https://github.com/redbeestudios/hexagon/releases/download/v0.25.1/hexagon-0.25.1.tar.gz
```

### Create your teams CLI

Either use our [template repo](https://github.com/redbeestudios/hexagon-tools) or create a YAML like the following
```yaml
cli:
  custom_tools_dir: .  # relative to this file
  name: Test CLI
  command: tc

envs:
  - name: dev
    alias: d
  - name: qa
    alias: q

tools:

  - name: google
    alias: g
    long_name: Google
    description: Open google
    type: web
    envs:
      dev: google.dev
      qa: google.qa
    action: open_link

  - name: docker-registry
    alias: dr
    long_name: Docker Registry
    type: shell
    envs:
      dev: my.custom.registry
    action: docker_registry
```

### Install the CLI

Run `hexagon` and select the CLI installation tool

## Options

### Theming

Hexagon supports 3 themes for now:

 - default (some nice colors and decorations)
 - disabled (no colors and no decorations)
 - result_only (with colors but only shows the result logs)

This can be specified by the envvar `HEXAGON_THEME`, i.e.,

```bash
# assuming you installed a CLI with command tc
HEXAGON_THEME=result_only tc
```


## Development

### Pre-requisites

```bash
pip install pipenv
```

### Run:

```bash
# start a shell
pipenv shell
# install hexagon dependencies
pipenv install
# run it
python -m hexagon
```

### Unit Tests:

```bash
pytest -svv tests/
```

### E2E Tests:

```bash
pytest -svv e2e/
```

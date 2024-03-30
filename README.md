# hexagon
Make your team's knowledge truly accessible, truly shared, and truly empowering by creating your own CLI.

[![01_ci-cd](https://github.com/lt-mayonesa/hexagon/actions/workflows/01-python-package.yml/badge.svg)](https://github.com/lt-mayonesa/hexagon/actions/workflows/01-python-package.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![hexagon setup example](https://user-images.githubusercontent.com/11464844/141402773-2fa1e859-cbe7-43a2-87e8-81620307167f.gif)](https://asciinema.org/a/Mk8of7EC0grfsSgWYrEdGCjdF)

---

## Getting Started

### Install hexagon
```bash
pip install hexagon
```

### Create your teams CLI

Either use our [template repo](https://github.com/lt-mayonesa/hexagon-tools) or create a YAML like the following
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

  - name: hello-world
    alias: hw
    long_name: Greet the world
    type: shell
    action: echo "Hello World!"
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
pipenv install --dev
# run it
python -m hexagon
```

### Unit Tests:

```bash
pytest -svv tests/
```

### E2E Tests:

```bash
# first generate the transalation files
.github/scripts/i18n/build.sh
# run tests
pytest -svv tests_e2e/
```

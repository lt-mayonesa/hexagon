# hexagon
Make your CLI

[![build](https://github.com/redbeestudios/hexagon/actions/workflows/python-package.yml/badge.svg)](https://github.com/redbeestudios/hexagon/actions/workflows/python-package.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


---

## Install
```bash
python3 -m pip install https://github.com/redbeestudios/hexagon/releases/download/v0.7.6/hexagon-0.7.6.tar.gz
```

## Pre-requisites (dev):

```bash
# En caso de no tener instalado pipenv localmente
pip install pipenv
# Para crear un virtual environment (shell aislado, no interferimos con instalaciones locales de paquetes de Python).
pipenv shell
# Para instalar las dependencias
pipenv install
```

## Run (dev):

```bash
# desde la shell de pipenv
python -m hexagon
```

## Unit Tests:

```bash
pytest -svv tests/
```

---

## Example CLI YAML

```yaml
cli:
  custom_tools_dir: .  # relative to this file
  name: Test CLI
  command: tc

envs:
  dev:
    alias: d
  qa:
    alias: q

tools:

  google:
    alias: g
    long_name: Google
    description: Abrir google
    type: web
    envs:
      dev: google.dev
      qa: google.qa
    action: open_link

  docker-registry:
    alias: dr
    long_name: Docker Registry
    type: shell
    envs:
      dev: registry.dev.redbee.io
    action: docker_registry
```
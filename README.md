# hexagon
Make your CLI

[![build](https://github.com/redbeestudios/hexagon/actions/workflows/python-package.yml/badge.svg)](https://github.com/redbeestudios/hexagon/actions/workflows/python-package.yml)

---

## Install
```bash
python3 -m pip install https://github.com/redbeestudios/hexagon/releases/download/v0.7.1/hexagon-0.7.1.tar.gz
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
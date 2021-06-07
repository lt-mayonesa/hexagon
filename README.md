# hexagon
Make your CLI

---

## Pre-requisites (dev):

```bash
# En caso de no tener instalado pipenv localmente
pip install pipenv
# Para crear un virtual environment (shell isolado, no interferimos con instalaciones locales de paquetes de Python).
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
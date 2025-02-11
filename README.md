![Command Center](https://img.shields.io/badge/terraform%20command%20center-45d298?logo=terraform&logoColor=white)
[![Maintainability](https://api.codeclimate.com/v1/badges/62ef5aeefc01a2c5521b/maintainability)](https://codeclimate.com/repos/67ab4de0fe407500a7cecccf/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/62ef5aeefc01a2c5521b/test_coverage)](https://codeclimate.com/repos/67ab4de0fe407500a7cecccf/test_coverage)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Installation:

```bash
pip install -r requirements/requirements-dev.txt
```

Run:
    
```bash
export PYTHONPATH="$PYTHONPATH:$PWD" && python src/terry/presentation/cli/app.py
```

Dev mode:

```bash
pip install textual-dev
cd src
export PYTHONPATH="$PYTHONPATH:$PWD" && textual run terry/presentation/cli/app.py
```

Run tests:

```bash 
coverage run && coverage report -m
```

Open html report:

```bash
coverage html && open htmlcov/index.html
```
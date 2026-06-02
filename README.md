# copier-python-package

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json)](https://github.com/copier-org/copier)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
![Python](https://img.shields.io/pypi/pyversions/copier?logo=python&logoColor=%23959DA5)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

>[!note]
> This is an opinionated [Copier](https://github.com/copier-org/copier) template for bootstrapping Python packages managed by [uv](https://github.com/astral-sh/uv).

## Features

- **[uv](https://github.com/astral-sh/uv)** - dependency management and virtual environments, with `[dependency-groups]` for dev tooling (PEP 735)
- **[hatchling](https://hatch.pypa.io/latest/config/build/) + [hatch-vcs](https://github.com/ofek/hatch-vcs)** - build backend with version derived from Git tags
- **[Ruff](https://github.com/astral-sh/ruff)** - fast linting and formatting
- **[mypy](https://mypy-lang.org/)** - strict static type checking
- **[pytest](https://docs.pytest.org/)** + **[coverage](https://coverage.readthedocs.io/)** - testing and coverage reporting
- **[prek](https://github.com/j178/prek)** - pre-commit hook runner configured with format, lint, type-check, and secret-detection hooks
- **[detect-secrets](https://github.com/Yelp/detect-secrets)** - baseline-driven secret scanning
- **[Just](https://github.com/casey/just)** - task runner for common development commands
- Apache 2.0 licence, `COPYRIGHT`, and `CHANGELOG.md` pre-populated with the current date

## Requirements

| Tool | Minimum version | Install |
|---|---|---|
| [Python](https://www.python.org/) | 3.10 | [python.org](https://www.python.org/downloads/) |
| [uv](https://github.com/astral-sh/uv) | any recent | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [Copier](https://github.com/copier-org/copier) | 9.0.0 | `uv tool install copier` |
| [Just](https://github.com/casey/just) | any recent | See documentation |

## Usage

### Generate a new project

```shell
copier copy gh:andyrids/copier-python-package path/to/your-project
```

Or from a specific tag:

```shell
copier copy --vcs-ref v1.0.0 gh:andyrids/copier-python-package path/to/your-project
```

### Template questions

| Question | Description | Default |
|---|---|---|
| `package_name` | Distribution name (e.g. `my-package`) | - |
| `package_description` | One-line summary | `An example Python package.` |
| `user_name` | Author full name | - |
| `user_email` | Author email address | - |
| `git_platform` | `GitHub` or `GitLab` | `GitHub` |
| `github_user` / `gitlab_user` | Platform username | - |
| `requires_python` | Minimum Python version specifier | `>=3.10` |
| `python_version` | Exact Python version for development | `3.13.13` |

> `import_package_name` is derived automatically from `package_name` (hyphens replaced with underscores) and is not prompted.

### Set up the generated project

```shell
cd your-project
git init && git add .
git commit -m "chore: initial commit from copier template"
just setup
```

`just setup` runs:
1. `uv sync` - creates `.venv` and installs all dependencies from `[dependency-groups]`
2. `uv run -m prek install` - installs pre-commit hooks
3. `just secrets-baseline` - generates a `detect-secrets` baseline (first run only)

### Generated project structure

```
your-project/
├── src/
│   └── your_package/
│       └── __init__.py       # exposes __version__ via importlib.metadata
├── tests/
│   ├── __init__.py
│   └── conftest.py
├── .gitignore
├── CHANGELOG.md
├── COPYRIGHT
├── Dockerfile
├── Justfile
├── LICENSE
├── README.md
├── prek.toml                 # pre-commit hook configuration
└── pyproject.toml            # project metadata, build system, tool config
```

### Updating an existing project

After the template receives changes, update a previously generated project with:

```shell
cd your-project
copier update
```

Copier will re-ask questions (pre-populated with previous answers) and apply a three-way merge of template changes into your project.

## Development

### Setup

```shell
git clone https://github.com/andyrids/copier-python-package
cd copier-python-package
just setup
```

### Dependencies

| Package | Purpose |
|---|---|
| `copier` | Template engine used in tests |
| `coverage` | Test coverage reporting |
| `detect-secrets` | Secret scanning baseline |
| `mypy` | Static type checking |
| `prek` | Pre-commit hook runner |
| `pytest` | Test suite |
| `ruff` | Linting and formatting |

### Running tests

```shell
uv run pytest
```

### Pre-commit hooks

The following hooks run automatically on every commit:

| Hook | Tool | Action |
|---|---|---|
| `check-toml` | builtin | Validate TOML syntax |
| `check-yaml` | builtin | Validate YAML syntax |
| `detect-private-key` | builtin | Scan for PEM keys |
| `format` | Ruff | Auto-format Python files |
| `lint` | Ruff | Lint and auto-fix Python files |
| `typing` | mypy | Type-check Python files (excludes `tests/`) |
| `detect-secrets` | detect-secrets | Check against `.secrets.baseline` |

## Licence

[Apache 2.0](LICENSE) - see [COPYRIGHT](COPYRIGHT) for details.
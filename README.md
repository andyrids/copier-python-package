# copier-python-package

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json)](https://github.com/copier-org/copier)
![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue?logo=python&logoColor=%23959DA5)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![prek](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> [!NOTE]
> An opinionated [Copier](https://github.com/copier-org/copier) template for bootstrapping
> Python packages managed by [uv](https://github.com/astral-sh/uv).

## Features

- **[uv](https://github.com/astral-sh/uv)** - dependency management & virtual environments,
  with `[dependency-groups]` for dev tooling (PEP 735)
- **[hatchling](https://hatch.pypa.io/latest/config/build/) +
  [hatch-vcs](https://github.com/ofek/hatch-vcs)** - build backend with the version derived
  from Git tags
- **[pkgdx](https://gitlab.com/andyrids/pkgdx)** - canonical standards & pre-commit hooks:
  [Ruff](https://github.com/astral-sh/ruff) lint & format, [mypy](https://mypy-lang.org/),
  [PyMarkdown](https://github.com/jackdewinter/pymarkdown) &
  [detect-secrets](https://github.com/Yelp/detect-secrets), run by
  [prek](https://github.com/j178/prek)
- **[pytest](https://docs.pytest.org/)** + **[coverage](https://coverage.readthedocs.io/)** -
  testing & coverage reporting
- **[Just](https://github.com/casey/just)** or **GNU Make** - task runner for common
  development commands
- **[Rich](https://github.com/Textualize/rich)** logging configuration, a base exception class
  & a `py.typed` marker
- **CI/CD** - GitHub Actions or GitLab CI running hooks, a Python version test matrix & a build,
  with opt-in PyPI trusted publishing on `v*` tags
- **`AGENTS.md`** & `docs/` - coding standards & toolchain references for coding agents
- Apache 2.0 licence & `COPYRIGHT`

## Requirements

| Tool | Minimum version | Install |
|---|---|---|
| [Python](https://www.python.org/) | 3.11 | `uv python install` |
| [uv](https://github.com/astral-sh/uv) | any recent | See [documentation][uv-install] |
| [Copier](https://github.com/copier-org/copier) | 9.5.0 | `uv tool install copier` |
| [Git](https://git-scm.com/) | any recent | See [documentation][git-install] |

[uv-install]: https://docs.astral.sh/uv/getting-started/installation/
[git-install]: https://git-scm.com/downloads

Just is installed into the generated project as the `rust-just` dev dependency, unless you opt
out. GNU Make must be installed separately if you choose it.

## Usage

### Generate a new project

```shell
copier copy gh:andyrids/copier-python-package path/to/your-project
```

Or from a specific tag:

```shell
copier copy --vcs-ref <tag> gh:andyrids/copier-python-package path/to/your-project
```

The template has no tasks or Jinja extensions, so `--trust` is never needed.

### Template questions

| Question | Description | Default |
|---|---|---|
| `package_name` | Distribution name (e.g. `my-package`) | Destination folder name |
| `package_description` | One-line summary | `Python package description` |
| `user_name` | Author full name | - |
| `user_email` | Author email address | - |
| `git_platform` | `GitHub` or `GitLab` | `GitHub` |
| `github_user` / `gitlab_user` | Platform username or group | - |
| `git_repository` | Repository URL (`https://`) | Derived from platform, user & name |
| `python_min` | Minimum supported Python: `3.11` to `3.14` | `3.11` |
| `python_version` | Exact Python version for development (`>= python_min`) | `3.13.13` |
| `task_runner` | `Just` or `GNU Make` | `Just` |
| `install_just_dependency` | Add `rust-just` as a dev dependency (Just only) | `true` |
| `publish_to_pypi` | Publish to PyPI on `v*` tags via trusted publishing | `false` |

`import_package_name` is derived from `package_name` (lowercased, with `-`, `_` & `.` runs
replaced by `_`) and is not prompted. `python_min` sets `requires-python`, the version
classifiers & the CI test matrix (up to Python 3.14).

Answers are validated: package names must start with a letter, names & descriptions must not
contain `"`, `\` or newlines, and emails, usernames & URLs are format checked.

### Set up the generated project

The version is derived from Git, so initialise a repository before syncing:

```shell
cd your-project
git init && git add .
git commit -m "chore: initial commit from copier template"
just setup  # or: make setup
```

`setup` runs:

1. `uv sync` - creates `.venv` & installs the project with its dev dependencies
2. `uv run pkgdx init` - writes `prek.toml`, installs the pre-commit hooks & creates
   `.secrets.baseline`

Then commit the files `setup` creates, which CI requires:

```shell
git add uv.lock prek.toml .secrets.baseline
git commit -m "chore: add lock & hooks"
```

`pkgdx` is installed from its GitLab package registry, which is declared as an explicit uv index
so that every other dependency still resolves from PyPI.

### Generated CI/CD

GitHub projects get `.github/workflows/ci.yml` & GitLab projects get `.gitlab-ci.yml`, with the
same jobs:

| Job | Runs |
|---|---|
| `hooks` | Checks `uv.lock`, `prek.toml` & `.secrets.baseline` exist, then `prek run --all-files` |
| `test` | `pytest` under `coverage` (`--fail-under=75`) for each Python from `python_min` to 3.14 |
| `build` | `uv build --no-sources`, keeping `dist/` as an artifact |
| `publish` | Only with `publish_to_pypi`: on a `v*` tag, `uv publish --trusted-publishing always` |

CI never runs `pkgdx init`, because creating `.secrets.baseline` in CI would accept any secret
already committed. History & tags are fetched in full, as `hatch-vcs` derives the version from
them.

To publish, [add a trusted publisher][pypi-publisher] on PyPI before pushing the first tag:

- GitHub - workflow `ci.yml`, environment `pypi`
- GitLab - top-level pipeline file `.gitlab-ci.yml`, environment `pypi`. PyPI supports trusted
  publishing from gitlab.com projects; elsewhere set a masked `UV_PUBLISH_TOKEN` variable instead

[pypi-publisher]: https://docs.pypi.org/trusted-publishers/adding-a-publisher/

### Generated project structure

```text
your-project/
├── .github/workflows/ci.yml  # or .gitlab-ci.yml
├── docs/                     # standards & toolchain references (Layer 3)
├── src/
│   └── your_package/
│       ├── logging/          # Rich logging configuration (config.toml)
│       ├── __init__.py       # exposes __version__ via importlib.metadata
│       ├── __main__.py       # CLI entry point
│       ├── _types.py
│       ├── exceptions.py     # package base exception
│       └── py.typed
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_init.py
├── .copier-answers.yml
├── .gitattributes
├── .gitignore
├── .python-version
├── AGENTS.md
├── CHANGELOG.md
├── COPYRIGHT
├── Justfile                  # or Makefile
├── LICENSE
├── README.md
└── pyproject.toml            # project metadata, build system, tool config
```

### Updating an existing project

After the template receives changes, update a previously generated project with:

```shell
cd your-project
copier update
```

Copier re-asks questions (pre-populated with previous answers) and applies a three-way merge of
template changes into your project. Projects generated before `python_min` replaced
`requires_python` are asked for `python_min` on their next update.

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
| `pkgdx` | Canonical standards & pre-commit hooks |
| `pytest` | Test suite |
| `pytest-copier` | Template rendering fixtures |

### Running tests

```shell
uv run pytest                 # render & context tests
uv run pytest -m integration  # toolchain tests in a generated project
```

The integration tests render the template, commit & tag it, then run `uv sync`, the generated
test suite, `uv build` with an isolated wheel import, `pkgdx init` & `prek run --all-files` in
the generated project, plus `actionlint` on a generated GitHub workflow. They are slow & need
network access, so they are deselected by default.

### CI/CD

`.github/workflows/ci.yml` runs on pushes to `main` & pull requests:

- `hooks` - `prek run --all-files`
- `test` - `uv run pytest` on Ubuntu, Windows & macOS
- `integration` - `uv run pytest -m integration` on Ubuntu & Windows

Pushing a `v*` tag runs `.github/workflows/release.yml`, which reuses CI & then creates a GitHub
release. Copier reads tags directly, so a tag is the release.

### Pre-commit hooks

Hooks are configured by `pkgdx` in `prek.toml`:

| Hook | Tool | Action |
|---|---|---|
| `pkgdx-lint` | Ruff | Lint & auto-fix Python files |
| `pkgdx-format` | Ruff | Auto-format Python files |
| `pkgdx-markdown` | PyMarkdown | Lint Markdown files |
| `pkgdx-secrets` | detect-secrets | Check against `.secrets.baseline` |
| `pkgdx-typing` | mypy | Type-check Python files (excludes `tests/`) |
| `check-toml` | builtin | Validate TOML syntax |
| `check-yaml` | builtin | Validate YAML syntax |
| `detect-private-key` | builtin | Scan for PEM keys |

## Licence

[Apache 2.0](LICENSE) - see [COPYRIGHT](COPYRIGHT) for details.

<!-- pyml disable MD024 -->
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> [!NOTE]
>
> - `[SemVer] - yyyy-mm-dd` or `[Unreleased]` for release heading.
> - `Added` for new features.
> - `Changed` for changes in existing functionality.
> - `Deprecated` for soon-to-be removed features.
> - `Removed` for now removed features.
> - `Fixed` for any bug fixes.
> - `Security` in case of vulnerabilities.

## [Unreleased]

### Changed

- Generated CLIs require `pyclig~=0.5.0`, and generated projects require `pkgdx~=0.10`.
- `standard-cli.md` 2.3.0 (proposed) adds `-o`, `-p` and `-u` as pyclig options and covers config,
  environment and secrets. The text names APIs that need `pyclig` 0.5.0.

## [0.5.0] - 2026-11-04

### Changed

- Generated CLIs require `pyclig~=0.4.0`, and generated projects require `pkgdx~=0.9`.
- `standard-cli.md` 2.2.0 recommends printing records with `ctx.emit`. The text names APIs that
  need `pyclig` 0.4.0.

## [0.4.0] - 2026-11-03

### Changed

- Generated CLIs require `pyclig~=0.3.0`. The scaffold passes `examples=` to `pyclig.group` and
  `test_main.py` calls `assert_conforms(cli)`, so a new project passes the conformance kit.
- `standard-cli.md` 2.1.0, `toolchain-logging.md` 2.0.1 and `toolchain-pytest.md` 2.1.0 cover
  `pyclig` 0.3: `-q`, `--no-color`, `--no-input` and `--plain`, examples-first help, the
  `FORCE_COLOR` meaning and `assert_conforms`. The text names APIs that need `pyclig` 0.3.0.

## [0.3.0] - 2026-11-02

### Added

- A `cli` question (default `false`) generates a `pyclig` group in `__main__.py`, a `test_main.py`,
  a `[project.scripts]` entry and the `pyclig` dependency.

### Changed

- `toolchain-pkgdx.md` 1.1.1 covers the `[tool.pkgdx] exclude` list added in `pkgdx` 0.7.0.
- `toolchain-mypy.md` 1.0.1 notes that `[tool.pkgdx] exclude` paths add to the default exclusions.
- Generated projects require `pkgdx~=0.7`, so the `[tool.pkgdx] exclude` guidance applies.
- `standard-cli.md`, `toolchain-logging.md` and `toolchain-pytest.md` 2.0.0 add MUST rules: CLIs
  build on `pyclig`, consoles are created per run and logging is not configured from a file.
- `__version__` falls back to `0.0.0+unknown` without package metadata, instead of being undefined.
- The package `__init__.py` adds the `NullHandler` itself, so library use stays silent.
- `rich` is no longer a default dependency. Projects that import it must declare it themselves, as
  dev environments still get it through `pkgdx`, so tests won't catch a missing one.

### Removed

- The `logging/` subpackage and the unconditional `__main__.py`. `copier update` deletes both, so a
  project with a CLI must answer `cli` with yes.

### Fixed

- `toolchain-pkgdx.md` 1.1.1 and `toolchain-uv.md` 1.0.1 no longer say `pkgdx` resolves from a
  GitLab index.
- The hatch-vcs comment in `pyproject.toml` names the project instead of `pkgdx`.

## [0.2.0] - 2026-10-30

### Added

- `standard-context-hierarchy.md` explains the context layers, frontmatter keys and immutability.
- `version` and `updated` frontmatter keys on every immutable guidance file.
- `toolchain-pkgdx.md` covers `pkgdx` hook ownership in `prek.toml`, resets, upgrades and config
  overrides.

### Changed

- `toolchain-prek.md` points to `toolchain-pkgdx.md`, which allows project hooks alongside `pkgdx`
  hooks and warns that `init --reset` deletes them.
- `toolchain-ruff.md`, `toolchain-mypy.md` and `toolchain-pymarkdown.md` point to
  `toolchain-pkgdx.md` for config overrides.
- `AGENTS.md` points to `standard-context-hierarchy.md` instead of summarizing the frontmatter.

### Fixed

- `toolchain-pytest.md` links `toolchain-coverage.md` instead of `reference-toolchain-coverage.md`.

## [0.1.1] - 2026-10-29

### Changed

- Standards & guidelines documentation now in `docs/guidance`.

## [0.1.0] - 2026-10-21

### Added

- `publish_to_pypi` question for opt-in PyPI trusted publishing on `v*` tags.
- Generated CI/CD: `.github/workflows/ci.yml` (GitHub) or `.gitlab-ci.yml` (GitLab).
- Validators for names, descriptions, emails, usernames & repository URLs.
- `_message_after_copy` with next steps.
- Template CI & release workflows, and integration tests.

### Changed

- `requires_python` (free-text specifier) is replaced by the `python_min` choice (`3.11` to
  `3.14`). On `copier update` the old answer is dropped & `python_min` is asked instead.
- `python_version` must be at least `python_min`, and its default follows `python_min`.
- Package names must start with a letter. The default is derived from a cleaned-up folder name.
- Minimum Copier version is `9.5.0`.

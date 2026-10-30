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

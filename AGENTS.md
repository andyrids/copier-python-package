# Copier Python package template [`copier-python-package`]

This Copier template project is used to bootstrap Python package projects using a modern stack.

- Astral uv package management
- A `hatchling` + `hatch-vcs` build backend with version derived from Git tags
- Canonical standards provided by `pkgdx` ([andyrids/pkgdx](https://gitlab.com/andyrids/pkgdx))
- A generated `AGENTS.md` (commands, tooling, layout) and a `CLAUDE.md` that imports it

## Layout

- `copier.yaml` - Questions, validators and the `template` subdirectory
- `template/` - Rendered into each generated project (`.jinja` files are templated)
- `tests/test_template.py` - Generation tests via `pytest-copier`

## Commands

- `uv run pytest -v` - Generate projects and test them
- `uv run prek run --all-files` - Run every hook

## Conventions

- Implement only what is asked; prefer the standard library, then an existing dependency, and ask
  before adding one
- `template/AGENTS.md.jinja` holds project facts and commands only. Personal standards live in
  `~/.claude/rules`, managed by the `hq` repo, and are not bundled into generated projects
- Keep generated Markdown free of stray blank lines: use `{%-` on block tags in `.jinja` files

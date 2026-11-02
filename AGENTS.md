---
context-hierarchy: Layer 0
context-hierarchy-role: Global identity
immutable: false
recommended-context-tokens: 900
---

# Copier Python package template [`copier-python-package`]

This Copier template project is used to bootstrap Python package projects using a modern stack.

- Astral uv package management
- A `hatchling` + `hatch-vcs` build backend with version derived from Git tags
- Canonical standards provided by `pkgdx` ([andyrids/pkgdx](https://gitlab.com/andyrids/pkgdx))
- Agent guidance documentation (`template/docs/guidance/*.md`)

This project adheres to [YAGNI](template/docs/guidance/standard-yagni.md) principles.

## Context hierarchy

Markdown files declare their layer in frontmatter - read
[standard-context-hierarchy.md](template/docs/guidance/standard-context-hierarchy.md) before
creating or editing one. Files marked `immutable: true` are never edited in passing: propose the
change and wait for approval.

## Reference

Standards and references live in `template/docs/guidance/` as `standard-*.md` and `toolchain-*.md`
files (Layer 3). Load a file when its subject is in play, which can be determined by the
frontmatter.

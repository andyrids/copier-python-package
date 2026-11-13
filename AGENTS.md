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
- Agent guidance from the `codebase-guidance` plugin (`template/.claude/settings.json`)

This project adheres to YAGNI principles (`python-code-standards` skill).

## Context hierarchy

Markdown files declare their layer in frontmatter - the `markdown-authoring` skill holds the
context-hierarchy reference, so load it before creating or editing one. Files marked
`immutable: true` are never edited in passing: propose the change and wait for approval.

## Reference

Standards and toolchain references come from the `codebase-guidance` plugin (marketplace
[andyrids/agent-guidance](https://github.com/andyrids/agent-guidance)), which generated projects
enable through `.claude/settings.json`. Its skills load when their subject is in play and are
upstream-owned: propose amendments there instead of overriding them locally.

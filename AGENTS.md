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
- Agent guidance documentation (`docs/guidance/*.md`)

This project adheres to [YAGNI](docs/guidance/standard-yagni.md) principles.

## Markdown frontmatter

Markdown files carry `context-hierarchy`, `context-hierarchy-role` and `immutable` keys, plus
`recommended-context-tokens` where a target is given. Beyond those:

- Budgets are a signal, not an enforced limit. A file that outgrows one is worth a look - it may
  have started doing another layer's job.
- Layer 3 carries tags: [keyword, ...]. immutable: true marks the factory configuration, amended
  deliberately, not in passing.

## Reference

Standards and references live in `docs/guidance/` as `standard-*.md` and `toolchain-*.md` files
(Layer 3). Load a file when its subject is in play, which can be determined by the frontmatter.

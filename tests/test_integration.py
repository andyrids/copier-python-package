"""Integration tests that run the generated project's own toolchain.

The template is rendered into a temporary directory, committed & tagged, then
`uv`, `pytest`, `pkgdx` & `prek` are run inside the generated project. These
tests are slow & need network access, so they are deselected by default. Run
them with `uv run pytest -m integration`.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import pytest
from pytest_copier.plugin import CopierFixture

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_copier.plugin import CopierProject

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def env(copier_template: Path) -> dict[str, str]:
    """Environment for commands run inside a generated project.

    Built after `copier_template`, so it includes the isolated git config
    (`GIT_CONFIG_GLOBAL`) set by pytest-copier. `VIRTUAL_ENV` is dropped so the
    generated project uses its own `.venv`, not this repository's.

    Args:
        copier_template: Isolated, git-tagged copy of the template provided
            by pytest-copier.

    Returns:
        A copy of the current environment without `VIRTUAL_ENV`.
    """
    return {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}


@pytest.fixture(scope="module")
def synced_project(
    tmp_path_factory: pytest.TempPathFactory,
    copier_template: Path,
    copier_defaults: dict[str, Any],
    sessionpatch: pytest.MonkeyPatch,
    env: dict[str, str],
) -> CopierProject:
    """Render the template, commit & tag it (for hatch-vcs), then `uv sync`.

    Args:
        tmp_path_factory: A fixture for creating temporary directories.
        copier_template: Isolated, git-tagged copy of the template provided
            by pytest-copier.
        copier_defaults: Default answers for copier template questions.
        sessionpatch: Session-scoped MonkeyPatch provided by pytest-copier.
        env: Environment for commands run inside the generated project.

    Returns:
        A CopierProject instance wrapping the synced generated project.
    """
    dst = tmp_path_factory.mktemp("integration")
    fixture = CopierFixture(
        template=copier_template,
        defaults=copier_defaults,
        monkeypatch=sessionpatch,
    )
    project = fixture.copy(dst)
    project.run("git init", env=env)
    project.run("git add -A", env=env)
    project.run('git commit -m "chore: initial commit"', env=env)
    project.run("git tag v0.1.0", env=env)
    project.run("uv sync", env=env)
    return project


def test_pytest(synced_project: CopierProject, env: dict[str, str]) -> None:
    """Assert the generated test suite passes."""
    synced_project.run("uv run pytest", env=env)


def test_wheel_installs_in_isolation(
    synced_project: CopierProject, env: dict[str, str]
) -> None:
    """Assert the built wheel is versioned from the tag & imports cleanly.

    The wheel is installed without dev dependencies, which catches runtime
    imports that are missing from `[project] dependencies`.
    """
    synced_project.run("uv build --wheel", env=env)
    (wheel,) = (synced_project / "dist").glob("*.whl")
    assert "-0.1.0-" in wheel.name
    synced_project.run(
        f'uv run --isolated --no-project --with "{wheel}" '
        'python -c "import test_package.logging"',
        env=env,
    )


def test_prek_hooks_pass(
    synced_project: CopierProject, env: dict[str, str]
) -> None:
    """Assert `pkgdx init` succeeds & a fresh project passes every hook."""
    synced_project.run("uv run pkgdx init", env=env)
    synced_project.run("git add -A", env=env)
    synced_project.run("uv run prek run --all-files", env=env)


def test_github_workflow_actionlint(
    copier: CopierFixture, tmp_path: Path, env: dict[str, str]
) -> None:
    """Assert the generated GitHub Actions workflow passes `actionlint`."""
    project = copier.copy(tmp_path, publish_to_pypi=True, python_min="3.12")
    project.run(
        "uvx --from actionlint-py actionlint .github/workflows/ci.yml",
        env=env,
    )

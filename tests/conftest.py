"""Shared fixtures for copier template tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import pytest
from pytest_copier.plugin import CopierFixture, CopierProject


@pytest.fixture(scope="session")
def copier_template_paths() -> Sequence[str]:
    """Minimal whitelist of paths required to render the template.

    Returns:
        Sequence of paths relative to the project root to copy into the
        isolated template source used by pytest-copier.
    """
    return ["copier.yaml", "validators.jinja", "includes", "template"]


@pytest.fixture(scope="session")
def copier_defaults() -> dict[str, Any]:
    """Default answers for all copier template questions.

    Returns:
        A dictionary of default answers for copier template questions.
    """
    return {
        "package_name": "test-package",
        "package_description": "A test package.",
        "user_name": "Test User",
        "user_email": "test@example.com",
        "git_platform": "GitHub",
        "github_user": "testuser",
        "requires_python": ">=3.10",
        "python_version": "3.12.13",
    }


@pytest.fixture(scope="session")
def generated_project(
    tmp_path_factory: pytest.TempPathFactory,
    copier_template: Path,
    copier_defaults: dict[str, Any],
    sessionpatch: pytest.MonkeyPatch,
) -> CopierProject:
    """Generate a project from the template into a temporary directory.

    Args:
        tmp_path_factory: A fixture for creating temporary directories.
        copier_template: Isolated, git-tagged copy of the template provided
            by pytest-copier.
        copier_defaults: Default answers for copier template questions.
        sessionpatch: Session-scoped MonkeyPatch provided by pytest-copier.

    Returns:
        A CopierProject instance wrapping the generated project path.
    """
    dst = tmp_path_factory.mktemp("generated")
    fixture = CopierFixture(
        template=copier_template,
        defaults=copier_defaults,
        monkeypatch=sessionpatch,
    )
    return fixture.copy(dst)

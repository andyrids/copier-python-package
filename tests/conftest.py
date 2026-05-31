"""Shared fixtures for copier template tests."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from copier import run_copy


_PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def template_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Copy the template project to a temp directory without .git for copier.

    Args:
        tmp_path_factory: A fixture for creating temporary directories.

    Returns:
        Temporary path to the copied template project.
    """
    dst = tmp_path_factory.mktemp("template_src")
    shutil.copytree(
        _PROJECT_ROOT,
        dst,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"),
    )
    return dst


@pytest.fixture(scope="session")
def default_data() -> dict[str, str]:
    """Return default answers for all copier template questions.

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
        "git_repository": "https://github.com/testuser/test-package",
        "requires_python": ">=3.10",
        "python_version": "3.12.13",
    }


@pytest.fixture(scope="session")
def generated_project(
    tmp_path_factory: pytest.TempPathFactory,
    template_path: Path,
    default_data: dict[str, str],
) -> Path:
    """Generate a project from the template into a temporary directory.

    Args:
        tmp_path_factory: A fixture for creating temporary directories.
        template_path: A fixture providing the path to the copied template
            project.
        default_data: A fixture providing default answers for copier template
            questions.

    Returns:
        Temporary path to the generated project.
    """
    dst = tmp_path_factory.mktemp("generated")
    run_copy(
        str(template_path),
        str(dst),
        data=default_data,
        defaults=True,
        overwrite=True,
        quiet=True,
    )
    return dst

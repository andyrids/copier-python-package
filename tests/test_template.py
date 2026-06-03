"""Tests for the copier Python package template."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_copier.plugin import CopierFixture, CopierProject


EXPECTED_FILES = [
    ".copier-answers.yml",
    "pyproject.toml",
    "COPYRIGHT",
    "CHANGELOG.md",
    "prek.toml",
    "Dockerfile",
    "README.md",
    "LICENSE",
    "Justfile",
    ".gitignore",
    "src/test_package/__init__.py",
    "tests/__init__.py",
    "tests/conftest.py",
]


@pytest.mark.parametrize("relative_path", EXPECTED_FILES)
def test_expected_files_exist(
    generated_project: "CopierProject", relative_path: str
) -> None:
    """Assert that each expected file exists in the generated project."""
    assert (generated_project / relative_path).exists()


def test_copier_answers(generated_project: "CopierProject") -> None:
    """Assert key answers are recorded correctly in .copier-answers.yml."""
    answers = generated_project.answers
    assert answers["package_name"] == "test-package"
    assert answers["package_description"] == "A test package."
    assert answers["user_name"] == "Test User"
    assert answers["user_email"] == "test@example.com"
    assert answers["git_platform"] == "GitHub"
    assert answers["github_user"] == "testuser"
    assert (
        answers["git_repository"] == "https://github.com/testuser/test-package"
    )
    assert answers["requires_python"] == ">=3.10"


def test_pyproject_package_name(generated_project: "CopierProject") -> None:
    """Assert the package name is rendered correctly in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'name = "test-package"' in content


def test_pyproject_description(generated_project: "CopierProject") -> None:
    """Test package description rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'description = "A test package."' in content


def test_pyproject_author(generated_project: "CopierProject") -> None:
    """Test author name & email rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'name = "Test User"' in content
    assert 'email = "test@example.com"' in content


def test_pyproject_requires_python(generated_project: "CopierProject") -> None:
    """Test requires-python rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'requires-python = ">=3.10"' in content


def test_pyproject_repository_url(generated_project: "CopierProject") -> None:
    """Test repository URL rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'Repository = "https://github.com/testuser/test-package"' in content


def test_copyright_year(generated_project: "CopierProject") -> None:
    """Test the current year rendering in COPYRIGHT via strftime."""
    content = (generated_project / "COPYRIGHT").read_text()
    assert f"Copyright {datetime.date.today().year}" in content


def test_copyright_user_name(generated_project: "CopierProject") -> None:
    """Test the user name rendering in COPYRIGHT."""
    content = (generated_project / "COPYRIGHT").read_text()
    assert "Test User" in content


def test_changelog_date(generated_project: "CopierProject") -> None:
    """Test the current date rendering in CHANGELOG.md via strftime."""
    content = (generated_project / "CHANGELOG.md").read_text()
    assert datetime.date.today().strftime("%Y-%m-%d") in content


def test_prek_detect_secrets_hook(generated_project: "CopierProject") -> None:
    """Test the detect-secrets hook configuration in prek.toml."""
    content = (generated_project / "prek.toml").read_text()
    assert 'entry = "uv run detect-secrets-hook"' in content
    assert "--baseline" in content
    assert ".secrets.baseline" in content
    assert "pass_filenames = true" in content


def test_init_package_name(generated_project: "CopierProject") -> None:
    """Test the package name rendering in __init__.py."""
    content = (generated_project / "src/test_package/__init__.py").read_text()
    assert 'metadata.version("test-package")' in content


# ---------------------------------------------------------------------------
# Context-only tests — fast, no disk generation
# ---------------------------------------------------------------------------


def test_import_package_name_derived(copier: "CopierFixture") -> None:
    """Verify import_package_name derives hyphens to underscores from Jinja."""
    ctx = copier.context(package_name="my-cool-package")
    assert ctx["import_package_name"] == "my_cool_package"


def test_git_repository_github_derived(copier: "CopierFixture") -> None:
    """Verify GitHub repo URL is derived correctly from Jinja defaults."""
    ctx = copier.context(
        package_name="my-package",
        git_platform="GitHub",
        github_user="octocat",
    )
    assert ctx["git_repository"] == "https://github.com/octocat/my-package"


def test_git_repository_gitlab_derived(copier: "CopierFixture") -> None:
    """Verify GitLab repo URL is derived correctly from Jinja defaults."""
    ctx = copier.context(
        package_name="my-package",
        git_platform="GitLab",
        gitlab_user="gitlabber",
    )
    assert ctx["git_repository"] == "https://gitlab.com/gitlabber/my-package"


# ---------------------------------------------------------------------------
# Variant generation tests — per-test isolated full copy
# ---------------------------------------------------------------------------


def test_variant_gitlab_platform(
    copier: "CopierFixture", tmp_path: "pytest.TempPathFactory"
) -> None:
    """Assert GitLab variant generates correct repository URL in pyproject."""
    project = copier.copy(
        tmp_path,  # pyright: ignore[reportArgumentType]
        git_platform="GitLab",
        gitlab_user="gitlabber",
        package_name="my-package",
        user_name="Test User",
        user_email="test@example.com",
        package_description="A test package.",
        requires_python=">=3.10",
        python_version="3.12.13",
    )
    content = (project / "pyproject.toml").read_text()
    assert 'Repository = "https://gitlab.com/gitlabber/my-package"' in content
    assert project.answers["git_platform"] == "GitLab"

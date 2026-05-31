"""Tests for the copier Python package template."""

from __future__ import annotations

import datetime
from pathlib import Path

import pytest


EXPECTED_FILES = [
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
    generated_project: Path, relative_path: str
) -> None:
    """Assert that each expected file exists in the generated project."""
    assert (generated_project / relative_path).exists()


def test_pyproject_package_name(generated_project: Path) -> None:
    """Assert the package name is rendered correctly in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'name = "test-package"' in content


def test_pyproject_description(generated_project: Path) -> None:
    """Test package description rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'description = "A test package."' in content


def test_pyproject_author(generated_project: Path) -> None:
    """Test author name & email rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'name = "Test User"' in content
    assert 'email = "test@example.com"' in content


def test_pyproject_requires_python(generated_project: Path) -> None:
    """Test requires-python rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'requires-python = ">=3.10"' in content


def test_pyproject_repository_url(generated_project: Path) -> None:
    """Test repository URL rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'Repository = "https://github.com/testuser/test-package"' in content


def test_copyright_year(generated_project: Path) -> None:
    """Test the current year rendering in COPYRIGHT via strftime."""
    content = (generated_project / "COPYRIGHT").read_text()
    assert f"Copyright {datetime.date.today().year}" in content


def test_copyright_user_name(generated_project: Path) -> None:
    """Test the user name rendering in COPYRIGHT."""
    content = (generated_project / "COPYRIGHT").read_text()
    assert "Test User" in content


def test_changelog_date(generated_project: Path) -> None:
    """Test the current date rendering in CHANGELOG.md via strftime."""
    content = (generated_project / "CHANGELOG.md").read_text()
    assert datetime.date.today().strftime("%Y-%m-%d") in content


def test_prek_detect_secrets_hook(generated_project: Path) -> None:
    """Test the detect-secrets hook configuration in prek.toml."""
    content = (generated_project / "prek.toml").read_text()
    assert 'entry = "uv run detect-secrets-hook"' in content
    assert "--baseline" in content
    assert ".secrets.baseline" in content
    assert "pass_filenames = true" in content


def test_init_package_name(generated_project: Path) -> None:
    """Test the package name rendering in __init__.py."""
    content = (generated_project / "src/test_package/__init__.py").read_text()
    assert "test-package" in content

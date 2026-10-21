"""Tests for the copier Python package template."""

from __future__ import annotations

import datetime
import tomllib
from typing import TYPE_CHECKING, Any

import pytest
import yaml

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_copier.plugin import CopierFixture, CopierProject


EXPECTED_FILES = [
    ".copier-answers.yml",
    ".gitattributes",
    ".gitignore",
    ".python-version",
    "AGENTS.md",
    "pyproject.toml",
    "COPYRIGHT",
    "CHANGELOG.md",
    "README.md",
    "LICENSE",
    "Justfile",
    ".github/workflows/ci.yml",
    "docs/standard-yagni.md",
    "src/test_package/__init__.py",
    "src/test_package/__main__.py",
    "src/test_package/py.typed",
    "src/test_package/logging/config.toml",
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_init.py",
]


def load_pyproject(project: CopierProject) -> dict[str, Any]:
    """Parse the generated pyproject.toml, asserting it is valid TOML."""
    return tomllib.loads((project / "pyproject.toml").read_text())


@pytest.mark.parametrize("relative_path", EXPECTED_FILES)
def test_expected_files_exist(
    generated_project: CopierProject, relative_path: str
) -> None:
    """Assert that each expected file exists in the generated project."""
    assert (generated_project / relative_path).exists()


def test_copier_answers(generated_project: CopierProject) -> None:
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
    assert answers["python_min"] == "3.11"
    assert answers["publish_to_pypi"] is False


def test_pyproject_package_name(generated_project: CopierProject) -> None:
    """Assert the package name is rendered correctly in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'name = "test-package"' in content


def test_pyproject_description(generated_project: CopierProject) -> None:
    """Test package description rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'description = "A test package."' in content


def test_pyproject_author(generated_project: CopierProject) -> None:
    """Test author name & email rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'name = "Test User"' in content
    assert 'email = "test@example.com"' in content


def test_pyproject_requires_python(generated_project: CopierProject) -> None:
    """Test requires-python rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'requires-python = ">=3.11"' in content
    assert '"Programming Language :: Python :: 3.11",' in content
    assert '"Programming Language :: Python :: 3.14",' in content


def test_pyproject_repository_url(generated_project: CopierProject) -> None:
    """Test repository URL rendering in pyproject.toml."""
    content = (generated_project / "pyproject.toml").read_text()
    assert 'Repository = "https://github.com/testuser/test-package"' in content


def test_pyproject_runtime_dependencies(
    generated_project: CopierProject,
) -> None:
    """Test `rich` is a runtime dependency of the logging module."""
    pyproject = load_pyproject(generated_project)
    assert "rich" in pyproject["project"]["dependencies"]


def test_pyproject_index_explicit(generated_project: CopierProject) -> None:
    """Test the GitLab index only serves packages pinned to it via sources."""
    pyproject = load_pyproject(generated_project)
    (index,) = pyproject["tool"]["uv"]["index"]
    assert index["explicit"] is True
    assert pyproject["tool"]["uv"]["sources"]["pkgdx"] == {"index": "gitlab"}


def test_pyproject_rust_just(generated_project: CopierProject) -> None:
    """Test `rust-just` is a dev dependency for the default Just runner."""
    pyproject = load_pyproject(generated_project)
    assert "rust-just" in pyproject["dependency-groups"]["dev"]


def test_justfile_setup(generated_project: CopierProject) -> None:
    """Test the Justfile `setup` recipe syncs and runs `pkgdx init`."""
    content = (generated_project / "Justfile").read_text()
    assert "setup:\n    uv sync\n    uv run pkgdx init\n" in content


def test_copyright_year(generated_project: CopierProject) -> None:
    """Test the current year rendering in COPYRIGHT via strftime."""
    content = (generated_project / "COPYRIGHT").read_text()
    assert f"Copyright {datetime.date.today().year}" in content


def test_copyright_user_name(generated_project: CopierProject) -> None:
    """Test the user name rendering in COPYRIGHT."""
    content = (generated_project / "COPYRIGHT").read_text()
    assert "Test User" in content


def test_init_package_name(generated_project: CopierProject) -> None:
    """Test the package name rendering in __init__.py."""
    content = (generated_project / "src/test_package/__init__.py").read_text()
    assert 'metadata.version("test-package")' in content


# ---------------------------------------------------------------------------
# Context-only tests — fast, no disk generation
# ---------------------------------------------------------------------------


def test_import_package_name_derived(copier: CopierFixture) -> None:
    """Verify import_package_name derives hyphens to underscores from Jinja."""
    ctx = copier.context(package_name="my-cool-package")
    assert ctx["import_package_name"] == "my_cool_package"


def test_git_repository_github_derived(copier: CopierFixture) -> None:
    """Verify GitHub repo URL is derived correctly from Jinja defaults."""
    ctx = copier.context(
        package_name="my-package",
        git_platform="GitHub",
        github_user="octocat",
    )
    assert ctx["git_repository"] == "https://github.com/octocat/my-package"


def test_git_repository_gitlab_derived(copier: CopierFixture) -> None:
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
    copier: CopierFixture, tmp_path: pytest.TempPathFactory
) -> None:
    """Assert GitLab variant generates correct repository URL in pyproject."""
    project = copier.copy(
        tmp_path,  # pyright: ignore[reportArgumentType]
        git_platform="GitLab",
        gitlab_user="gitlabber",
        package_name="my-package",
    )
    content = (project / "pyproject.toml").read_text()
    assert 'Repository = "https://gitlab.com/gitlabber/my-package"' in content
    assert project.answers["git_platform"] == "GitLab"


def test_variant_gnu_make(
    copier: CopierFixture, tmp_path: pytest.TempPathFactory
) -> None:
    """Assert GNU Make variant renders a Makefile and omits `rust-just`."""
    project = copier.copy(
        tmp_path,  # pyright: ignore[reportArgumentType]
        task_runner="GNU Make",
    )
    assert (project / "Makefile").exists()
    assert not (project / "Justfile").exists()
    assert "\t@uv run pkgdx init\n" in (project / "Makefile").read_text()
    assert (
        "rust-just" not in load_pyproject(project)["dependency-groups"]["dev"]
    )


def test_variant_just_without_dependency(
    copier: CopierFixture, tmp_path: pytest.TempPathFactory
) -> None:
    """Assert `install_just_dependency=False` omits `rust-just`."""
    project = copier.copy(
        tmp_path,  # pyright: ignore[reportArgumentType]
        task_runner="Just",
        install_just_dependency=False,
    )
    assert (project / "Justfile").exists()
    assert (
        "rust-just" not in load_pyproject(project)["dependency-groups"]["dev"]
    )


def test_variant_python_min(
    copier: CopierFixture, tmp_path: pytest.TempPathFactory
) -> None:
    """Assert `python_min` drives requires-python, classifiers & CI matrix."""
    project = copier.copy(
        tmp_path,  # pyright: ignore[reportArgumentType]
        python_min="3.13",
        python_version="3.13.13",
    )
    pyproject = load_pyproject(project)
    assert pyproject["project"]["requires-python"] == ">=3.13"
    versions = [
        c.rsplit(" :: ", 1)[1]
        for c in pyproject["project"]["classifiers"]
        if c.startswith("Programming Language :: Python :: 3.")
    ]
    assert versions == ["3.13", "3.14"]
    workflow = load_workflow(project / ".github/workflows/ci.yml")
    matrix = workflow["jobs"]["test"]["strategy"]["matrix"]
    assert matrix["python-version"] == ["3.13", "3.14"]


# ---------------------------------------------------------------------------
# Validator tests — context-only, invalid answers raise ValueError
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("question", "value"),
    [
        ("package_name", "1package"),
        ("package_name", "-package"),
        ("package_description", ""),
        ("package_description", 'A "quoted" package.'),
        ("user_name", ""),
        ("user_name", "Back\\slash"),
        ("user_email", "not-an-email"),
        ("github_user", ""),
        ("github_user", "-user"),
        ("git_repository", "github.com/user/repo"),
        ("python_version", "3"),
        ("python_version", "3.10.4"),
    ],
)
def test_validator_rejects(
    copier: CopierFixture, question: str, value: str
) -> None:
    """Assert invalid answers fail the question validator."""
    with pytest.raises(
        ValueError, match=f"Validation error for question '{question}'"
    ):
        copier.context(**{question: value})


def test_python_min_choices(copier: CopierFixture) -> None:
    """Assert `python_min` only accepts the supported choices."""
    with pytest.raises(ValueError, match="Invalid choice for 'python_min'"):
        copier.context(python_min="3.10")


def test_python_version_below_python_min(copier: CopierFixture) -> None:
    """Assert `python_version` must not be below `python_min`."""
    with pytest.raises(
        ValueError, match="Validation error for question 'python_version'"
    ):
        copier.context(python_min="3.13", python_version="3.12.9")


def test_python_version_default_follows_python_min(
    copier_template: Path, tmp_path: Path
) -> None:
    """Assert the `python_version` default satisfies a high `python_min`."""
    from copier import run_copy

    worker = run_copy(
        str(copier_template),
        tmp_path,
        defaults=True,
        data={
            "package_name": "test-package",
            "user_name": "Test User",
            "user_email": "test@example.com",
            "github_user": "testuser",
            "python_min": "3.14",
        },
    )
    assert worker.answers.combined["python_version"] == "3.14"


# ---------------------------------------------------------------------------
# CI/CD tests — generated pipelines per platform & publish option
# ---------------------------------------------------------------------------


def load_workflow(path: Path) -> dict[Any, Any]:
    """Parse a generated CI file, asserting no Jinja leaked into it."""
    content = path.read_text()
    assert "{%" not in content
    return yaml.safe_load(content)


def test_github_workflow(generated_project: CopierProject) -> None:
    """Assert the GitHub workflow has CI jobs, GitHub expressions & no CD."""
    path = generated_project / ".github/workflows/ci.yml"
    workflow = load_workflow(path)
    assert set(workflow["jobs"]) == {"hooks", "test", "build"}
    assert "${{ matrix.python-version }}" in path.read_text()
    matrix = workflow["jobs"]["test"]["strategy"]["matrix"]
    assert matrix["python-version"] == ["3.11", "3.12", "3.13", "3.14"]
    assert not (generated_project / ".gitlab-ci.yml").exists()


def test_variant_github_publish(
    copier: CopierFixture, tmp_path: pytest.TempPathFactory
) -> None:
    """Assert `publish_to_pypi` adds a tag-gated trusted publishing job."""
    project = copier.copy(
        tmp_path,  # pyright: ignore[reportArgumentType]
        publish_to_pypi=True,
    )
    workflow = load_workflow(project / ".github/workflows/ci.yml")
    # PyYAML parses the bare `on` key as boolean True
    assert workflow[True]["push"]["tags"] == ["v*"]
    publish = workflow["jobs"]["publish"]
    assert publish["permissions"] == {"id-token": "write"}
    assert publish["if"] == "startsWith(github.ref, 'refs/tags/v')"
    assert "uv publish --trusted-publishing always" in str(publish["steps"])


def test_variant_gitlab_ci(
    copier: CopierFixture, tmp_path: pytest.TempPathFactory
) -> None:
    """Assert GitLab variant renders `.gitlab-ci.yml` & no `.github/`."""
    project = copier.copy(
        tmp_path,  # pyright: ignore[reportArgumentType]
        git_platform="GitLab",
        gitlab_user="gitlabber",
        publish_to_pypi=True,
    )
    assert not (project / ".github").exists()
    pipeline = load_workflow(project / ".gitlab-ci.yml")
    assert pipeline["stages"] == ["check", "test", "build", "publish"]
    matrix = pipeline["test"]["parallel"]["matrix"]
    assert matrix == [{"UV_PYTHON": ["3.11", "3.12", "3.13", "3.14"]}]
    assert pipeline["publish"]["id_tokens"] == {
        "PYPI_ID_TOKEN": {"aud": "pypi"}
    }

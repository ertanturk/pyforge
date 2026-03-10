"""Tests for CLI module."""

from pathlib import Path

import pyforge.cli as cli
from _pytest.capture import CaptureFixture
from pyforge.cli import ProjectDetails, main
from pytest import MonkeyPatch


def test_main_creates_project_scaffold(
    monkeypatch: MonkeyPatch, tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """Test that main creates scaffold in a new project directory."""

    answers = iter(
        [
            "demoapp",
            "Demo application",
            ">=3.12",
            "cli,tool",
            "",
            "",
            "1",
            "y",
            "y",
            "n",
            "n",
            "y",
        ]
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    main()

    project_root = tmp_path / "demoapp"
    assert project_root.exists()
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / "MANIFEST.in").exists()
    assert (project_root / "requirements-dev.txt").exists()
    assert (project_root / "LICENSE").exists()
    assert (project_root / "scripts" / "setup.py").exists()
    assert (project_root / "src" / "demoapp" / "cli.py").exists()
    assert (project_root / "tests" / "test_cli.py").exists()

    output = capsys.readouterr().out
    assert "Project scaffold created at:" in output


def test_bootstrap_virtual_environment_dev_install(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Test that .venv bootstrap uses expected commands with dev extras."""

    project_root = tmp_path / "demo"
    project_root.mkdir()

    commands: list[list[str]] = []

    def fake_run_checked(cmd: list[str], cwd: Path) -> None:
        assert cwd == project_root
        commands.append(cmd)

    monkeypatch.setattr(cli, "_run_checked", fake_run_checked)
    monkeypatch.setattr(cli, "_python_executable", lambda: "/usr/bin/python3")
    monkeypatch.setattr(cli, "_venv_python_path", lambda _root: project_root / "venvpy")

    details: ProjectDetails = {
        "name": "demo",
        "description": "desc",
        "python_version": ">=3.12",
        "keywords": "",
        "author": "author",
        "email": "a@b.com",
        "license": "1",
        "dynamic_versioning": True,
        "install_recommended": True,
        "github_workflow": False,
        "create_venv": True,
    }

    cli.bootstrap_virtual_environment(details, project_root)

    assert commands[0][:3] == ["/usr/bin/python3", "-m", "venv"]
    assert commands[0][3] == ".venv"
    assert commands[1] == [
        str(project_root / "venvpy"),
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
    ]
    assert commands[2] == [
        str(project_root / "venvpy"),
        "-m",
        "pip",
        "install",
        "-e",
        ".[dev]",
    ]


def test_bootstrap_virtual_environment_skips_when_disabled(tmp_path: Path) -> None:
    """Test that bootstrap does nothing when create_venv is disabled."""

    details: ProjectDetails = {
        "name": "demo",
        "description": "desc",
        "python_version": ">=3.12",
        "keywords": "",
        "author": "author",
        "email": "a@b.com",
        "license": "1",
        "dynamic_versioning": True,
        "install_recommended": False,
        "github_workflow": False,
        "create_venv": False,
    }

    cli.bootstrap_virtual_environment(details, tmp_path)


def test_normalize_python_version_spec_accepts_plain_version() -> None:
    """Test that plain version input gets normalized to a minimum spec."""

    assert cli._normalize_python_version_spec("3.10") == ">=3.10"
    assert cli._normalize_python_version_spec(">=3.12") == ">=3.12"


def test_build_pyproject_uses_selected_python_version() -> None:
    """Test generated pyproject uses user-selected Python major/minor."""

    details: ProjectDetails = {
        "name": "demo",
        "description": "desc",
        "python_version": ">=3.10",
        "keywords": "",
        "author": "author",
        "email": "a@b.com",
        "license": "1",
        "dynamic_versioning": False,
        "install_recommended": False,
        "github_workflow": False,
        "create_venv": False,
    }

    content = cli._build_pyproject(details, "demo")

    assert "Programming Language :: Python :: 3.10" in content
    assert 'target-version = "py310"' in content
    assert 'python_version = "3.10"' in content
    assert 'version = "0.1.0"' in content

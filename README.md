# pyforge

pyforge is a lightweight CLI that generates a modern Python project scaffold
with sensible defaults for packaging, linting, testing, typing, and CI.

## Features

- Interactive project setup with input validation
- src-layout package structure
- PEP 621 pyproject.toml generation
- Optional dynamic versioning helper at scripts/setup.py
- Optional GitHub Actions CI workflow
- Ready-to-use test and quality tool configuration

## Install

For local development:

```bash
python -m pip install -e .
```

Global user install (recommended for CLI usage):

Linux/macOS:

```bash
python3 -m pip install --user pyforge
```

Windows:

```powershell
py -m pip install --user pyforge
```

If you use pipx:

```bash
pipx install pyforge
```

## Usage

Run the CLI:

```bash
pyforge
```

Answer the prompts, review the summary, and confirm generation.

By default, pyforge can also bootstrap a .venv inside the generated project and
install either:

- `-e .[dev]` when recommended packages are enabled
- `-e .` otherwise

## Development Setup

```bash
python -m pip install -e .[dev]
pre-commit install
```

## Build Package

Create source and wheel distributions:

```bash
python -m build
```

The artifacts will be created under dist/.

## Validate Package Metadata

Check long description and distribution metadata:

```bash
python -m twine check dist/*
```

## Upload To PyPI

1. Create an API token in your PyPI account.
2. Set it as an environment variable:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-XXXXXXXXXXXXXXXXXXXXXXXX
```

3. Upload:

```bash
python -m twine upload dist/*
```

Use TestPyPI first if you want a dry run:

```bash
python -m twine upload --repository testpypi dist/*
```

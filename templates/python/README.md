# Python Templates for CRESP

This directory contains templates for Python projects to be used with CRESP (Computational Research Environment Standardization Protocol).

This is part of the `cresp-templates` repository, which is a standalone repository of templates for CRESP. The CRESP tool will download templates from this repository when creating new projects.

## Repository Structure

- `default/` - Python project template with Conda + Poetry
  - `src/` - Source code directory with `__init__.py` 
  - `tests/` - Tests directory with sample pytest file
  - `docs/` - Documentation directory
  - `notebooks/` - Jupyter notebooks directory with example notebook
  - `data/` - Data directory
  - `.gitignore` - Git ignore file
  - `environment.yml` - Conda environment configuration
  - `pyproject.toml` - Poetry configuration file
  - `README.md` - Project README

## Usage

These templates are automatically downloaded by the CRESP CLI when creating a new Python project:

```bash
cresp new python my-project
```

## For Template Developers

### Placeholders

The templates use the following placeholders that will be replaced by CRESP:

- `%PROJECT_NAME%` - The name of the project
- `%VERSION%` - The Python version
- `%PY_VERSION%` - The Python version without dots (e.g., 310 for 3.10)
- `PROJECT_NAME` - Alternative format for project name (used in some files)

### Adding New Templates

To add a new template variant, create a new directory at the same level as `default/` with a similar structure.

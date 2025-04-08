# Python Templates for CRESP

This directory contains templates for Python projects to be used with CRESP (Computational Research Environment Standardization Protocol).

This is part of the `cresp-templates` repository, which is a standalone repository of templates for CRESP. The CRESP tool will download templates from this repository when creating new projects.

## Template Options

CRESP supports multiple template engines for Python projects:

1. **Simple Templates** (default) - Basic file-based templates in this repository
2. **Cookiecutter** - If installed, CRESP can use [Cookiecutter](https://github.com/cookiecutter/cookiecutter) for more advanced templating with our default template

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
  - `cookiecutter.json` - Cookiecutter configuration
  - `hooks/` - Cookiecutter hooks for automation

## Using Templates Directly

### With CRESP

These templates are automatically downloaded by the CRESP CLI when creating a new Python project:

```bash
cresp new python my-project
```

If you have Cookiecutter installed, CRESP will ask which template engine you'd like to use.

### With Cookiecutter

You can also use our default template directly with Cookiecutter:

```bash
# Install cookiecutter if not already installed
pip install cookiecutter

# Create a new project using our template
cookiecutter https://github.com/wisupai/cresp-templates --directory="templates/python/default"
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

# CRESP Templates

[![GitHub license](https://img.shields.io/github/license/wisupai/cresp-templates)](https://github.com/wisupai/cresp-templates/blob/main/LICENSE)

This repository contains templates for the [CRESP](https://github.com/wisupai/CRESP) tool (Computational Research Environment Standardization Protocol).

## Overview

CRESP is a tool for creating reproducible computational research environments. This repository contains the templates used by CRESP to initialize projects in different languages and frameworks.

The templates ensure that projects follow best practices for reproducibility, including:

- Standardized project structure
- Environment isolation and dependency management
- Proper documentation
- Testing frameworks
- Jupyter notebook integration
- Version control configuration

## Available Templates

- [`python`](templates/python/) - Templates for Python projects
  - Default template uses Conda for environment management and Poetry for package management

## For Template Developers

### Adding New Templates

To add a new language or framework template:

1. Create a new directory under `templates/`
2. Create a default template subdirectory (e.g., `templates/newlang/default/`)
3. Include all necessary template files
4. Add a `README.md` in the language directory explaining the template

### Template Structure

Each template should include:

- Documentation
- Environment configuration files
- Project structure with standard directories
- Template README.md with usage instructions
- Placeholder variables (using `%PLACEHOLDER%` format)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

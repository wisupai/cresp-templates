# CRESP Project Templates

This directory contains standardized project templates following the CRESP (Computational Research Environment Standardization Protocol) for reproducible science.

## Available Templates

### Python

- **Default** - A complete scientific Python project with:
  - Package management with Poetry
  - Environment management with Conda
  - Testing with pytest
  - Code quality tools (black, isort, mypy)
  - Scientific computing libraries (NumPy, Pandas, Matplotlib, etc.)

### R 

- Standard R project template for data analysis and visualization

### MATLAB

- Standard MATLAB project template

## Usage

These templates can be used with Cookiecutter:

```bash
# Install cookiecutter if not already installed
pip install cookiecutter

# Create a new Python project
cookiecutter https://github.com/wisupai/cresp-templates --directory="templates/python/default"

# Create a new R project
cookiecutter https://github.com/wisupai/cresp-templates --directory="templates/r/default"

# Create a new MATLAB project
cookiecutter https://github.com/wisupai/cresp-templates --directory="templates/matlab/default"
```

## Contributing

Feel free to contribute new templates or improve existing ones through pull requests.

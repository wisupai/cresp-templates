# %PROJECT_NAME%

## Project Overview
This is a Python project.

## Requirements
- Python
- Environment Management: Conda
- Package Manager: Poetry (inside Conda environment)

## Installation
```bash
# Clone the repository
git clone <repository-url>
cd %PROJECT_NAME%

# Create and activate Conda environment
conda env create -f environment.yml
conda activate $(basename $PWD)

# Install dependencies using Poetry
poetry install
```

## Usage
To be added

## Development
```bash
# Run development tasks with Poetry
poetry run pytest           # Run tests
poetry run black .          # Format code
poetry run isort .          # Sort imports
```

## Project Structure
- `src/` - Source code
- `tests/` - Test files
- `notebooks/` - Jupyter notebooks
- `docs/` - Documentation
- `data/` - Data files

## Important Notes
- Poetry is configured to use the Conda environment, so there's no need for a separate virtualenv
- The environment name matches the project directory name by default

## License
MIT 
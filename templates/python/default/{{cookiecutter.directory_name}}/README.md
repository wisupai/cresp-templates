# {{ cookiecutter.project_name }}

## Project Overview
This is a CRESP-based Python project for scientific computing and research. This project follows the CRESP (Computational Research Environment Standardization Protocol) for reproducible science.

## Requirements
- Python
- Environment Management: Conda
- Package Manager: Poetry (inside Conda environment)

## Installation
```bash
# Clone the repository
git clone <repository-url>
cd {{ cookiecutter.project_slug }}

# Create and activate Conda environment
conda env create -f environment.yml
conda activate $(basename $PWD)

# Install dependencies using Poetry
poetry install
```

## Usage
```bash
# Run Jupyter Lab for interactive development
{% if cookiecutter.include_jupyter == 'True' %}
jupyter lab

# Run a specific notebook
jupyter notebook notebooks/example.ipynb
{% else %}
# Note: Jupyter was not included in this project
# If needed, install with: pip install jupyterlab
{% endif %}

# Run a Python script
python -m src.main
```

## Development
```bash
# Run development tasks with Poetry
{% if cookiecutter.include_tests == 'True' %}
poetry run pytest           # Run tests
poetry run pytest --cov=src # Run tests with coverage
{% endif %}
poetry run black .          # Format code
poetry run isort .          # Sort imports
```

## Project Structure
- `src/` - Source code for the project
{% if cookiecutter.include_tests == 'True' %}
- `tests/` - Test files using pytest
{% endif %}
{% if cookiecutter.include_jupyter == 'True' %}
- `notebooks/` - Jupyter notebooks for exploration and visualization
{% endif %}
{% if cookiecutter.include_documentation == 'True' %}
- `docs/` - Documentation and research paper drafts
{% endif %}
- `data/` - Data files (raw, processed, and results)

## Scientific Computing Features
This template includes:
{% if cookiecutter.include_data_analysis == 'True' %}
- Numerical computing: NumPy, SciPy
- Data analysis: Pandas
{% endif %}
{% if cookiecutter.include_ml_libs == 'True' %}
- Machine learning: scikit-learn
{% endif %}
{% if cookiecutter.include_visualization == 'True' %}
- Visualization: Matplotlib, Seaborn, Plotly
{% endif %}
{% if cookiecutter.include_jupyter == 'True' %}
- Interactive computing: JupyterLab
{% endif %}

## Reproducibility
This project follows CRESP guidelines to ensure computational reproducibility:
- Explicit environment specification (Conda + Poetry)
- Version-controlled dependencies
- Separation of code, data, and results
{% if cookiecutter.include_tests == 'True' %}
- Automated testing with pytest
{% endif %}
- Documentation of computational workflow

## Important Notes
- Poetry is configured to use the Conda environment, so there's no need for a separate virtualenv
- The environment name matches the project directory name by default
- Add large data files to `.gitignore` and consider using Git LFS or data versioning tools

## Using This Template Directly
This template can be used directly with Cookiecutter:

```bash
# Install cookiecutter if not already installed
pip install cookiecutter

# Create a new project using this template
cookiecutter https://github.com/wisupai/cresp-templates --directory="templates/python/default"
```

## Useful Resources
- [Scientific Python](https://scientific-python.org/)
- [Reproducible Science](https://the-turing-way.netlify.app/reproducible-research/reproducible-research.html)
- [CRESP Documentation](https://github.com/wisupai/CRESP-DOCS)

## License
{{ cookiecutter.open_source_license }} 
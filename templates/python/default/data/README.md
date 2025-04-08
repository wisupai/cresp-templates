# Data Directory

This directory contains all data files for the project.

## Directory Structure

- `raw/` - Raw, unprocessed data files (read-only, never modify)
- `processed/` - Cleaned and processed data ready for analysis
- `results/` - Output data from analysis and visualizations

## Best Practices

1. **Raw Data**: Never modify raw data files. If you need to clean or transform them, save the result to the `processed/` directory.

2. **Documentation**: Document the source of all data files and any preprocessing steps.

3. **Large Files**: Consider using Git LFS (Large File Storage) for files over 10MB or adding them to `.gitignore`.

4. **Formats**: Prefer open and reproducible formats (CSV, JSON, Parquet, etc.) over proprietary formats.

5. **Metadata**: Include a `metadata.json` or README file in each subdirectory explaining the contents.

## Adding Data Files

When adding new data files, remember to:
- Update this README if necessary
- Add documentation about the source and format
- Consider privacy and licensing restrictions 
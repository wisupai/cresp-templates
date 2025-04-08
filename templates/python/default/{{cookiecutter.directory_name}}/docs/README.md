# Documentation

This directory contains project documentation.

## Directory Structure

- `api/` - API reference documentation (auto-generated)
- `user/` - User guides and tutorials
- `examples/` - Example usage and code snippets

## Documentation Tools

This project supports two popular documentation systems:

### MkDocs (Recommended for most projects)

[MkDocs](https://www.mkdocs.org/) with [Material theme](https://squidfunk.github.io/mkdocs-material/) provides a modern, responsive documentation site.

To use MkDocs:
```bash
pip install mkdocs-material
mkdocs serve  # Start local documentation server
mkdocs build  # Build documentation site
```

### Sphinx (Recommended for API-heavy projects)

[Sphinx](https://www.sphinx-doc.org/) is powerful for API documentation with automatic docstring extraction.

To use Sphinx:
```bash
pip install sphinx sphinx-rtd-theme
cd docs
sphinx-quickstart  # Setup new Sphinx project
sphinx-build -b html . _build/html  # Build documentation
```

## Best Practices

1. **Write as you code**: Update documentation as you develop
2. **Examples**: Include working examples for important functions
3. **Tutorials**: Create step-by-step tutorials for common workflows
4. **API docs**: Use docstrings to document all public functions, classes, and modules
5. **Versioning**: Document API changes between versions

## Building Documentation

To generate HTML documentation with Sphinx (if configured):

```bash
cd docs
make html
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pre-generation script for Cookiecutter.
This script runs before the project is generated.
"""

import re
import sys
import os

# Get cookiecutter configuration
project_name = "{{ cookiecutter.project_name }}"
project_slug = "{{ cookiecutter.project_slug }}"
python_version = "{{ cookiecutter.python_version }}"
include_jupyter = "{{ cookiecutter.include_jupyter }}" == "True"
include_tests = "{{ cookiecutter.include_tests }}" == "True"
include_visualization = "{{ cookiecutter.include_visualization }}" == "True"
include_data_analysis = "{{ cookiecutter.include_data_analysis }}" == "True"

# Validate project name
if not project_name.strip():
    print("ERROR: Project name cannot be empty")
    sys.exit(1)

# Validate project_slug
if not re.match(r'^[a-z][a-z0-9_]*$', project_slug):
    print("ERROR: Project slug must start with a letter and contain only lowercase letters, numbers, and underscores")
    sys.exit(1)

# Validate Python version
try:
    major, minor = map(int, python_version.split(".")[:2])
    if major < 3 or (major == 3 and minor < 8):
        print(f"WARNING: Python {python_version} is older than the recommended version (3.8+)")
except (ValueError, AttributeError):
    print(f"ERROR: Invalid Python version format: {python_version}. Expected format like '3.10'")
    sys.exit(1)

# Validation for feature combinations
if not include_data_analysis and include_visualization:
    print("WARNING: You selected visualization without data analysis libraries. You may want to include both.")

if include_tests and not include_data_analysis:
    print("NOTE: You selected tests without data analysis libraries. Make sure your tests don't need NumPy/pandas.")

if not include_jupyter and include_visualization:
    print("NOTE: You selected visualization without Jupyter. Consider including Jupyter for interactive visualization.")

# Check if we're inside a virtual environment
if "VIRTUAL_ENV" in os.environ:
    print("NOTE: You are currently in a virtual environment.")
    print("This project will create a Conda environment. Consider deactivating your current venv first.")

# All checks passed
print(f"Pre-generation checks passed. Creating project {project_name}...") 
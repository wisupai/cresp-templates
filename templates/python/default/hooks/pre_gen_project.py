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

# Check if we're inside a virtual environment
if "VIRTUAL_ENV" in os.environ:
    print("NOTE: You are currently in a virtual environment.")
    print("This project will create a Conda environment. Consider deactivating your current venv first.")

# All checks passed
print(f"Pre-generation checks passed. Creating project {project_name}...") 
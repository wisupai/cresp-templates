#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Post-generation script for Cookiecutter.
This script runs after the project is generated.
"""

import os
import sys
import json
import shutil
from pathlib import Path

# Get cookiecutter configuration
project_name = "{{ cookiecutter.project_name }}"
project_slug = "{{ cookiecutter.project_slug }}"
python_version = "{{ cookiecutter.python_version }}"
include_ml_libs = "{{ cookiecutter.include_ml_libs }}" == "True"
with_cuda = "{{ cookiecutter.with_cuda }}" == "True"
license_choice = "{{ cookiecutter.open_source_license }}"

# Colors for terminal output
TERMCOLOR_BLUE = "\033[94m"
TERMCOLOR_GREEN = "\033[92m"
TERMCOLOR_YELLOW = "\033[93m"
TERMCOLOR_RED = "\033[91m"
TERMCOLOR_BOLD = "\033[1m"
TERMCOLOR_ENDC = "\033[0m"

def print_success(message):
    """Print a success message."""
    print(f"{TERMCOLOR_GREEN}✓ {message}{TERMCOLOR_ENDC}")

def print_info(message):
    """Print an info message."""
    print(f"{TERMCOLOR_BLUE}→ {message}{TERMCOLOR_ENDC}")

def print_warning(message):
    """Print a warning message."""
    print(f"{TERMCOLOR_YELLOW}! {message}{TERMCOLOR_ENDC}")

def print_error(message):
    """Print an error message."""
    print(f"{TERMCOLOR_RED}✗ {message}{TERMCOLOR_ENDC}")

def main():
    """Main function to run post-generation setup."""
    print_info(f"Setting up project: {project_name}")

    # Update pyproject.toml with ML libs if requested
    if include_ml_libs:
        print_info("Including machine learning libraries in pyproject.toml")
        update_dependencies_for_ml()
    
    # Setup conda environment file
    print_info("Setting up conda environment")
    update_environment_yml()
    
    # Set up license if chosen
    if license_choice != "None":
        print_info(f"Setting up {license_choice} license")
        setup_license()

    # Final instructions
    print_success("Project setup complete!")
    print_info("To get started:")
    print(f"  cd {project_slug}")
    print("  conda env create -f environment.yml")
    print(f"  conda activate {project_slug}")
    print("  poetry install")

def update_dependencies_for_ml():
    """Update pyproject.toml to include ML libraries."""
    try:
        pyproject_path = Path("pyproject.toml")
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Add scikit-learn, tensorflow/pytorch if not already in file
        ml_additions = ""
        if "scikit-learn" not in content:
            ml_additions += 'scikit-learn = "^1.2.0"\n'
        
        # Insert the additions before the dev dependencies
        if ml_additions and "[tool.poetry.group.dev.dependencies]" in content:
            content = content.replace(
                "[tool.poetry.group.dev.dependencies]",
                f"{ml_additions}\n[tool.poetry.group.dev.dependencies]"
            )
            
            with open(pyproject_path, 'w') as f:
                f.write(content)
            print_success("Added ML libraries to pyproject.toml")
    except Exception as e:
        print_warning(f"Could not update pyproject.toml: {e}")

def update_environment_yml():
    """Update environment.yml with correct project name and CUDA settings."""
    try:
        env_path = Path("environment.yml")
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Replace project name
        content = content.replace("%PROJECT_NAME%", project_slug)
        
        # Replace Python version
        content = content.replace("%PYTHON_VERSION%", python_version)
        
        # Add CUDA packages if requested
        if with_cuda:
            content = content.replace(
                "dependencies:",
                "dependencies:\n  - cudatoolkit\n  - cudnn"
            )
        
        with open(env_path, 'w') as f:
            f.write(content)
        print_success("Updated environment.yml")
    except Exception as e:
        print_warning(f"Could not update environment.yml: {e}")

def setup_license():
    """Set up the license file based on the user's choice."""
    try:
        license_file = Path("LICENSE")
        
        # You'd ideally have the full text of each license type here
        license_text = f"Copyright (c) {os.environ.get('YEAR', '2023')} {{ cookiecutter.author_name }}\n\n"
        
        if license_choice == "MIT":
            license_text += "MIT License text would go here"
        elif license_choice == "BSD-3-Clause":
            license_text += "BSD-3-Clause License text would go here"
        elif license_choice == "GPL-3.0":
            license_text += "GPL-3.0 License text would go here"
        elif license_choice == "Apache-2.0":
            license_text += "Apache-2.0 License text would go here"
        
        with open(license_file, 'w') as f:
            f.write(license_text)
        print_success(f"Created {license_choice} license file")
    except Exception as e:
        print_warning(f"Could not create license file: {e}")

if __name__ == "__main__":
    main() 
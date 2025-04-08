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
include_visualization = "{{ cookiecutter.include_visualization }}" == "True"
include_jupyter = "{{ cookiecutter.include_jupyter }}" == "True"
include_data_analysis = "{{ cookiecutter.include_data_analysis }}" == "True"
include_documentation = "{{ cookiecutter.include_documentation }}" == "True"
include_tests = "{{ cookiecutter.include_tests }}" == "True"
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

    # Update pyproject.toml based on user selections
    update_pyproject_toml()
    
    # Setup conda environment file
    print_info("Setting up conda environment")
    update_environment_yml()
    
    # Set up license if chosen
    if license_choice != "None":
        print_info(f"Setting up {license_choice} license")
        setup_license()
    
    # Clean up optional components
    clean_optional_components()

    # Final instructions
    print_success("Project setup complete!")
    print_info("To get started:")
    print(f"  cd {project_slug}")
    print("  conda env create -f environment.yml")
    print(f"  conda activate {project_slug}")
    print("  poetry install")

def update_pyproject_toml():
    """Update pyproject.toml to include appropriate libraries."""
    try:
        pyproject_path = Path("pyproject.toml")
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Add libraries based on user preferences
        dependencies = []
        
        # ML libraries
        if include_ml_libs:
            print_info("Including machine learning libraries")
            if with_cuda:
                dependencies.extend([
                    'scikit-learn = "^1.2.0"',
                    'tensorflow = "^2.12.0"',
                ])
            else:
                dependencies.extend([
                    'scikit-learn = "^1.2.0"',
                ])
                
        # Visualization libraries
        if include_visualization:
            print_info("Including visualization libraries")
            dependencies.extend([
                'matplotlib = "^3.7.0"',
                'seaborn = "^0.12.0"',
                'plotly = "^5.13.0"',
            ])
        
        # Data analysis libraries
        if include_data_analysis:
            print_info("Including data analysis libraries")
            dependencies.extend([
                'pandas = "^2.0.0"',
                'numpy = "^1.24.0"',
                'scipy = "^1.10.0"',
            ])
        
        # Jupyter
        if include_jupyter:
            print_info("Including Jupyter libraries")
            dependencies.extend([
                'jupyterlab = "^3.6.0"',
            ])
            
        # Insert the dependencies before the dev dependencies
        if dependencies and "[tool.poetry.group.dev.dependencies]" in content:
            dependencies_str = "\n".join(dependencies)
            content = content.replace(
                "[tool.poetry.group.dev.dependencies]",
                f"{dependencies_str}\n\n[tool.poetry.group.dev.dependencies]"
            )
            
            with open(pyproject_path, 'w') as f:
                f.write(content)
            print_success("Updated pyproject.toml with selected libraries")
        
        # Remove pytest packages if tests are not included
        if not include_tests:
            # Remove pytest from the dependencies
            content = content.replace('pytest = "^7.3.1"\n', '')
            content = content.replace('pytest-cov = "^4.1.0"\n', '')
            # Remove pytest configuration
            lines = content.split('\n')
            new_lines = []
            skip_pytest_section = False
            for line in lines:
                if line.startswith('[tool.pytest.ini_options]'):
                    skip_pytest_section = True
                    continue
                elif skip_pytest_section and line.startswith('['):
                    skip_pytest_section = False
                
                if not skip_pytest_section:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
            
            with open(pyproject_path, 'w') as f:
                f.write(content)
            print_success("Removed testing packages from pyproject.toml")
            
    except Exception as e:
        print_warning(f"Could not update pyproject.toml: {e}")

def update_environment_yml():
    """Update environment.yml with correct project name and CUDA settings."""
    try:
        env_path = Path("environment.yml")
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Project name and Python version are now handled by Cookiecutter directly
        # No need to replace placeholders as they are handled in the template
        
        # Add CUDA packages if requested
        if with_cuda:
            content = content.replace(
                "dependencies:",
                "dependencies:\n  - cudatoolkit\n  - cudnn"
            )
        
        # Add specific conda packages based on selections
        conda_packages = []
        
        if include_jupyter:
            conda_packages.append("  - jupyterlab")
        
        if include_visualization:
            conda_packages.append("  - matplotlib-base")
        
        if include_data_analysis:
            conda_packages.append("  - numpy")
            conda_packages.append("  - pandas")
        
        if conda_packages:
            package_str = "\n".join(conda_packages)
            # Add these packages if they don't already exist
            for package in conda_packages:
                if package not in content:
                    content = content.replace(
                        "dependencies:",
                        f"dependencies:\n{package_str}"
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
        
        # Get the current year
        current_year = os.environ.get('YEAR', '2024')
        
        # Create basic copyright statement
        license_text = f"Copyright (c) {current_year} {{ cookiecutter.author_name }}\n\n"
        
        if license_choice == "MIT":
            license_text += "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            license_text += "of this software and associated documentation files (the \"Software\"), to deal\n"
            license_text += "in the Software without restriction, including without limitation the rights\n"
            license_text += "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            license_text += "copies of the Software, and to permit persons to whom the Software is\n"
            license_text += "furnished to do so, subject to the following conditions:\n\n"
            license_text += "The above copyright notice and this permission notice shall be included in all\n"
            license_text += "copies or substantial portions of the Software.\n\n"
            license_text += "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
            license_text += "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            license_text += "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            license_text += "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            license_text += "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            license_text += "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
            license_text += "SOFTWARE."
        elif license_choice == "BSD-3-Clause":
            license_text += "Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:\n\n"
            license_text += "1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.\n\n"
            license_text += "2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.\n\n"
            license_text += "3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.\n\n"
            license_text += "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
        elif license_choice == "GPL-3.0":
            license_text += "This program is free software: you can redistribute it and/or modify\n"
            license_text += "it under the terms of the GNU General Public License as published by\n"
            license_text += "the Free Software Foundation, either version 3 of the License, or\n"
            license_text += "(at your option) any later version.\n\n"
            license_text += "This program is distributed in the hope that it will be useful,\n"
            license_text += "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
            license_text += "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
            license_text += "GNU General Public License for more details.\n\n"
            license_text += "You should have received a copy of the GNU General Public License\n"
            license_text += "along with this program.  If not, see <https://www.gnu.org/licenses/>."
        elif license_choice == "Apache-2.0":
            license_text += "Licensed under the Apache License, Version 2.0 (the \"License\");\n"
            license_text += "you may not use this file except in compliance with the License.\n"
            license_text += "You may obtain a copy of the License at\n\n"
            license_text += "    http://www.apache.org/licenses/LICENSE-2.0\n\n"
            license_text += "Unless required by applicable law or agreed to in writing, software\n"
            license_text += "distributed under the License is distributed on an \"AS IS\" BASIS,\n"
            license_text += "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
            license_text += "See the License for the specific language governing permissions and\n"
            license_text += "limitations under the License."
        
        with open(license_file, 'w') as f:
            f.write(license_text)
        print_success(f"Created {license_choice} license file")
    except Exception as e:
        print_warning(f"Could not create license file: {e}")

def clean_optional_components():
    """Remove components that were not requested by the user."""
    # Remove documentation if not needed
    if not include_documentation and Path("docs").exists():
        print_info("Removing documentation directory (not requested)")
        shutil.rmtree("docs", ignore_errors=True)
    
    # Remove notebooks if Jupyter not selected
    if not include_jupyter and Path("notebooks").exists():
        print_info("Removing notebooks directory (not requested)")
        shutil.rmtree("notebooks", ignore_errors=True)
    
    # Remove tests if not needed
    if not include_tests and Path("tests").exists():
        print_info("Removing tests directory (not requested)")
        shutil.rmtree("tests", ignore_errors=True)
    
    # Adjust main.py based on selections
    if not (include_visualization and include_data_analysis):
        try:
            print_info("Adjusting main.py for selected features")
            main_path = Path("src/main.py")
            with open(main_path, 'r') as f:
                content = f.read()
            
            # Strip unnecessary imports
            if not include_visualization:
                content = content.replace("import matplotlib.pyplot as plt\nimport seaborn as sns", "")
                # Remove visualization function
                content = '\n'.join([line for line in content.split('\n') 
                                    if not line.startswith("def visualize_data")])
                # Remove call to visualize_data in main function
                content = content.replace("    # Visualize the data\n    visualize_data(data)\n", "")
            
            if not include_data_analysis:
                content = content.replace("import pandas as pd", "")
                content = content.replace("import numpy as np", "")
                # Remove analysis function
                content = '\n'.join([line for line in content.split('\n') 
                                    if not line.startswith("def analyze_data")])
                # Remove call to analyze_data in main function
                content = content.replace("    # Analyze the data\n    analyze_data(data)\n", "")
            
            with open(main_path, 'w') as f:
                f.write(content)
            print_success("Adjusted main.py based on selected features")
        except Exception as e:
            print_warning(f"Could not adjust main.py: {e}")

if __name__ == "__main__":
    main() 
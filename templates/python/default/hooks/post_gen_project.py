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
        
        # Project name and Python version are now handled by Cookiecutter directly
        # No need to replace placeholders as they are handled in the template
        
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
        
        # Get the current year
        current_year = os.environ.get('YEAR', '2025')
        
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

if __name__ == "__main__":
    main() 
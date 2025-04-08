#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example tests for {{ cookiecutter.project_name }} project.

This file demonstrates how to write tests for scientific code using pytest.
For reproducible research, it's important to verify that your code works as expected.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_dir))

# Import your own modules here
# For example:
# from src.my_module import my_function


def test_example():
    """A minimal passing test example."""
    assert 1 + 1 == 2


def test_with_fixture(tmp_path):
    """Test using pytest's builtin tmp_path fixture to work with files."""
    # Create a temporary file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "data.txt"
    p.write_text("42.0,12.5\n10.0,5.5")
    
    # Read the file (this would usually be done by your own function)
    with open(p, "r") as f:
        lines = f.readlines()
    
    # Verify the contents
    assert len(lines) == 2
    assert "42.0" in lines[0]


@pytest.mark.parametrize("input_val,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_parametrized(input_val, expected):
    """
    Parametrized test to verify multiple inputs at once.
    
    This is useful for testing mathematical functions with known results
    or testing edge cases of your algorithms.
    """
    assert input_val ** 2 == expected


class TestScientificCalculations:
    """
    A test class for grouping related scientific calculation tests.
    
    In scientific code, you might want to test:
    - Mathematical functions work correctly
    - Edge cases are handled appropriately
    - Results are within expected tolerances
    - Models produce expected outputs for known inputs
    """
    
    def test_floating_point_comparison(self):
        """Test comparing floating point values with tolerance."""
        # For scientific calculations, we often need to check within a tolerance
        result = 0.1 + 0.2  # In floating point, this isn't exactly 0.3
        assert pytest.approx(result, abs=1e-10) == 0.3
    
    def test_array_calculation(self):
        """Test a calculation on arrays (if numpy is available)."""
        try:
            import numpy as np
            # Example: Test a simple array operation
            data = np.array([1, 2, 3, 4, 5])
            result = np.mean(data)
            assert result == 3.0
        except ImportError:
            pytest.skip("NumPy not available")
    
    @pytest.mark.skipif(not os.path.exists("data/example.csv"),
                        reason="Test data not available")
    def test_with_external_data(self):
        """
        Test using external data files.
        
        This test will be skipped if the data file doesn't exist.
        This is useful for tests that require real-world data.
        """
        # This is an example of how to skip tests if data is missing
        pass


# If you have custom fixtures, define them here
@pytest.fixture
def sample_data():
    """Create sample data for tests."""
    # This could be a pandas DataFrame, numpy array, or any other structure
    return {"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]}


def test_with_sample_data(sample_data):
    """Test using the custom fixture."""
    assert len(sample_data["x"]) == 5
    assert sample_data["y"][2] == 6 
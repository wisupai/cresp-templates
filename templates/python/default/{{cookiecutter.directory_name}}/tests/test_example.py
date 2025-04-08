#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example test for PROJECT_NAME project.

This is a simple test file to demonstrate testing with pytest.
"""

import pytest


def test_example():
    """Test basic example function."""
    # Example test
    assert 1 + 1 == 2


def test_with_fixture(tmp_path):
    """Test using a pytest fixture."""
    # Example test with fixture
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("Hello, world!")
    assert p.read_text() == "Hello, world!"
    assert len(list(tmp_path.iterdir())) == 1


@pytest.mark.parametrize("input_val,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_parametrized(input_val, expected):
    """Test with parametrized inputs."""
    # Example parametrized test
    assert input_val ** 2 == expected 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for {{ cookiecutter.project_name }}.

This module demonstrates basic scientific computing capabilities
and serves as a starting point for your project.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def load_data(filename):
    """Load data from file."""
    data_dir = Path(__file__).parent.parent / "data"
    try:
        file_path = data_dir / filename
        if file_path.suffix == ".csv":
            return pd.read_csv(file_path)
        elif file_path.suffix in [".xls", ".xlsx"]:
            return pd.read_excel(file_path)
        else:
            print(f"Unsupported file format: {file_path.suffix}")
            return None
    except Exception as e:
        print(f"Error loading data: {e}")
        # Generate sample data as fallback
        return generate_sample_data()


def generate_sample_data(n_samples=100):
    """Generate sample data for demonstration."""
    np.random.seed(42)  # for reproducibility
    x = np.linspace(0, 10, n_samples)
    y = np.sin(x) + 0.1 * np.random.randn(n_samples)
    return pd.DataFrame({"x": x, "y": y})


def analyze_data(data):
    """Perform basic data analysis."""
    print("Data Summary:")
    print(data.describe())
    
    # Example correlation analysis
    if data.shape[1] > 1:
        print("\nCorrelation Matrix:")
        print(data.corr())


def visualize_data(data):
    """Create visualizations of the data."""
    # Set a nice style
    sns.set_theme(style="whitegrid")
    
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Scatter plot
    if "x" in data.columns and "y" in data.columns:
        sns.scatterplot(data=data, x="x", y="y", ax=ax1)
        ax1.set_title("Scatter Plot")
    
    # Plot 2: Distribution plot
    if data.shape[1] > 0:
        for column in data.select_dtypes(include=[np.number]).columns[:3]:  # Limit to first 3 numeric columns
            sns.kdeplot(data[column], ax=ax2, label=column)
        ax2.set_title("Distribution Plot")
        ax2.legend()
    
    plt.tight_layout()
    
    # Save the figure
    output_dir = Path(__file__).parent.parent / "data" / "results"
    output_dir.mkdir(exist_ok=True, parents=True)
    plt.savefig(output_dir / "data_visualization.png", dpi=300)
    
    print(f"Visualization saved to {output_dir / 'data_visualization.png'}")
    
    # Display if running in an interactive environment
    plt.show()


def main():
    """Main function."""
    print("=" * 50)
    print(f"Running {{ cookiecutter.project_name }}")
    print("=" * 50)
    
    # Load or generate data
    data = load_data("sample.csv")
    if data is None:
        data = generate_sample_data()
        print("Generated sample data")
    
    # Analyze the data
    analyze_data(data)
    
    # Visualize the data
    visualize_data(data)
    
    print("=" * 50)
    print("Analysis complete")
    print("=" * 50)


if __name__ == "__main__":
    main() 
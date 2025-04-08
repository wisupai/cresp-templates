#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for {{ cookiecutter.project_name }}.

This module demonstrates basic scientific computing capabilities
and serves as a starting point for your project.
"""

import sys
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("output.log")
    ]
)
logger = logging.getLogger(__name__)

# Import optional libraries based on project configuration
{% if cookiecutter.include_data_analysis == 'True' %}
import numpy as np
import pandas as pd
{% endif %}

{% if cookiecutter.include_visualization == 'True' %}
import matplotlib.pyplot as plt
import seaborn as sns
{% endif %}


def load_data(filename: str) -> Optional[{% if cookiecutter.include_data_analysis == 'True' %}pd.DataFrame{% else %}Any{% endif %}]:
    """
    Load data from file.
    
    Parameters
    ----------
    filename : str
        Name of the file to load (should be in the data directory)
        
    Returns
    -------
    {% if cookiecutter.include_data_analysis == 'True' %}pd.DataFrame{% else %}Any{% endif %}
        Loaded data or None if loading fails
    """
    data_dir = Path(__file__).parent.parent / "data"
    try:
        file_path = data_dir / filename
        logger.info(f"Loading data from {file_path}")
        
        if file_path.suffix == ".csv":
            {% if cookiecutter.include_data_analysis == 'True' %}
            return pd.read_csv(file_path)
            {% else %}
            with open(file_path, 'r') as f:
                return [line.strip().split(',') for line in f]
            {% endif %}
        elif file_path.suffix in [".xls", ".xlsx"]:
            {% if cookiecutter.include_data_analysis == 'True' %}
            return pd.read_excel(file_path)
            {% else %}
            logger.error("Excel support requires pandas. Install with: pip install pandas openpyxl")
            return None
            {% endif %}
        else:
            logger.error(f"Unsupported file format: {file_path.suffix}")
            return None
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        # Generate sample data as fallback
        return generate_sample_data()


def generate_sample_data(n_samples: int = 100) -> {% if cookiecutter.include_data_analysis == 'True' %}pd.DataFrame{% else %}Dict[str, List[float]]{% endif %}:
    """
    Generate sample data for demonstration.
    
    Parameters
    ----------
    n_samples : int, optional
        Number of samples to generate, by default 100
        
    Returns
    -------
    {% if cookiecutter.include_data_analysis == 'True' %}pd.DataFrame{% else %}Dict[str, List[float]]{% endif %}
        Generated sample data
    """
    logger.info(f"Generating sample data with {n_samples} samples")
    
    {% if cookiecutter.include_data_analysis == 'True' %}
    np.random.seed(42)  # for reproducibility
    x = np.linspace(0, 10, n_samples)
    y = np.sin(x) + 0.1 * np.random.randn(n_samples)
    return pd.DataFrame({"x": x, "y": y})
    {% else %}
    # Simple data generation without NumPy/Pandas
    import math
    import random
    random.seed(42)  # for reproducibility
    
    x = [i * 10 / (n_samples - 1) for i in range(n_samples)]
    y = [math.sin(val) + 0.1 * (random.random() * 2 - 1) for val in x]
    return {"x": x, "y": y}
    {% endif %}


{% if cookiecutter.include_data_analysis == 'True' %}
def analyze_data(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform basic data analysis.
    
    Parameters
    ----------
    data : pd.DataFrame
        Data to analyze
        
    Returns
    -------
    Dict[str, Any]
        Dictionary containing analysis results
    """
    logger.info("Analyzing data")
    
    # Store results in a dictionary
    results = {}
    
    # Basic summary statistics
    results["summary"] = data.describe()
    logger.info("Generated summary statistics")
    
    # Example correlation analysis
    if data.shape[1] > 1:
        results["correlation"] = data.corr()
        logger.info("Generated correlation matrix")
    
    return results
{% endif %}


{% if cookiecutter.include_visualization == 'True' %}
def visualize_data(data: {% if cookiecutter.include_data_analysis == 'True' %}pd.DataFrame{% else %}Dict[str, List[float]]{% endif %}) -> None:
    """
    Create visualizations of the data.
    
    Parameters
    ----------
    data : {% if cookiecutter.include_data_analysis == 'True' %}pd.DataFrame{% else %}Dict[str, List[float]]{% endif %}
        Data to visualize
    """
    logger.info("Creating visualizations")
    
    # Set a nice style
    sns.set_theme(style="whitegrid")
    
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Scatter plot
    {% if cookiecutter.include_data_analysis == 'True' %}
    if "x" in data.columns and "y" in data.columns:
        sns.scatterplot(data=data, x="x", y="y", ax=ax1)
        ax1.set_title("Scatter Plot")
    
    # Plot 2: Distribution plot
    if data.shape[1] > 0:
        for column in data.select_dtypes(include=[np.number]).columns[:3]:  # Limit to first 3 numeric columns
            sns.kdeplot(data[column], ax=ax2, label=column)
        ax2.set_title("Distribution Plot")
        ax2.legend()
    {% else %}
    if "x" in data and "y" in data:
        ax1.scatter(data["x"], data["y"])
        ax1.set_title("Scatter Plot")
        ax1.set_xlabel("x")
        ax1.set_ylabel("y")
    
    # Plot 2: Distribution as histogram
    if len(data) > 0:
        for key in list(data.keys())[:3]:  # Limit to first 3 keys
            ax2.hist(data[key], bins=20, alpha=0.6, label=key)
        ax2.set_title("Distribution Plot")
        ax2.legend()
    {% endif %}
    
    plt.tight_layout()
    
    # Save the figure
    output_dir = Path(__file__).parent.parent / "data" / "results"
    output_dir.mkdir(exist_ok=True, parents=True)
    figure_path = output_dir / "data_visualization.png"
    plt.savefig(figure_path, dpi=300)
    
    logger.info(f"Visualization saved to {figure_path}")
    
    # Display if running in an interactive environment
    plt.show()
{% endif %}


def save_results(results: Dict[str, Any], filename: str) -> None:
    """
    Save results to a file.
    
    Parameters
    ----------
    results : Dict[str, Any]
        Results to save
    filename : str
        Name of the file to save results to
    """
    output_dir = Path(__file__).parent.parent / "data" / "results"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    output_path = output_dir / filename
    logger.info(f"Saving results to {output_path}")
    
    # Save in JSON format for simple dictionary results
    try:
        import json
        with open(output_path, 'w') as f:
            json.dump(str(results), f, indent=2)
        logger.info("Results saved successfully")
    except Exception as e:
        logger.error(f"Error saving results: {e}")


def main() -> None:
    """Main function to run the analysis pipeline."""
    logger.info("=" * 50)
    logger.info(f"Running {{ cookiecutter.project_name }}")
    logger.info("=" * 50)
    
    # Load or generate data
    data = load_data("sample.csv")
    if data is None:
        data = generate_sample_data()
        logger.info("Using generated sample data")
    
    # Create a results dictionary to store outputs
    results = {}
    
    # Analyze the data
    {% if cookiecutter.include_data_analysis == 'True' %}
    analysis_results = analyze_data(data)
    results.update(analysis_results)
    {% endif %}
    
    # Visualize the data
    {% if cookiecutter.include_visualization == 'True' %}
    visualize_data(data)
    results["visualization_created"] = True
    {% endif %}
    
    # Save results
    save_results(results, "analysis_results.json")
    
    logger.info("=" * 50)
    logger.info("Analysis complete")
    logger.info("=" * 50)


if __name__ == "__main__":
    main() 
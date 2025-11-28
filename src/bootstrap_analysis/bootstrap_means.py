"""
Bootstrap Functions for Mean Estimation

This module provides functions for bootstrap resampling to estimate
confidence intervals for genre means by region.

NOTE: This is a template framework for Person 2.
      Person 2 should:
      1. Review and test the provided implementations
      2. Verify statistical correctness
      3. Add error handling and edge cases
      4. Optimize if needed
      5. Complete any TODO items
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional


def bootstrap_mean(data: np.ndarray, 
                  n_iterations: int = 10000, 
                  random_seed: Optional[int] = None) -> np.ndarray:
    """
    Bootstrap resampling for mean estimation.
    
    Args:
        data: 1D array of log-transformed sales values
        n_iterations: Number of bootstrap iterations (default: 10000)
        random_seed: Random seed for reproducibility
        
    Returns:
        Array of bootstrap means (length n_iterations)
    
    Raises:
        ValueError: If data is empty or n_iterations is not positive
    """
    # Input validation
    if len(data) == 0:
        raise ValueError("Data array cannot be empty")
    if n_iterations <= 0:
        raise ValueError("n_iterations must be positive")
    
    # Use modern numpy random number generator
    rng = np.random.default_rng(random_seed)
    n = len(data)
    bootstrap_means = np.empty(n_iterations)
    
    for i in range(n_iterations):
        # Resample with replacement
        sample = rng.choice(data, size=n, replace=True)
        bootstrap_means[i] = sample.mean()
    
    return bootstrap_means


def bootstrap_genre_mean_by_region(data: pd.DataFrame, 
                                  genre: str, 
                                  region: str, 
                                  n_iterations: int = 10000,
                                  random_seed: Optional[int] = None) -> Dict:
    """
    Bootstrap mean for a specific genre in a specific region.
    
    Args:
        data: DataFrame with 'Genre' and 'log_sales' columns
        genre: Genre name
        region: Region name (for identification purposes, not used in filtering)
        n_iterations: Number of bootstrap iterations
        random_seed: Random seed for reproducibility
        
    Returns:
        Dictionary with keys:
        - 'genre': Genre name
        - 'region': Region name
        - 'mean': Observed mean
        - 'bootstrap_means': Array of bootstrap means
        - 'sample_size': Sample size
    """
    if 'Genre' not in data.columns or 'log_sales' not in data.columns:
        raise ValueError("DataFrame must contain 'Genre' and 'log_sales' columns")
    
    # Filter data for the specific genre
    genre_data = data[data['Genre'] == genre]['log_sales'].values
    
    if len(genre_data) == 0:
        raise ValueError(f"No data found for genre: {genre}")
    
    # Calculate observed mean
    observed_mean = np.mean(genre_data)
    
    # Perform bootstrap
    bootstrap_means = bootstrap_mean(genre_data, n_iterations, random_seed)
    
    return {
        'genre': genre,
        'region': region,
        'mean': observed_mean,
        'bootstrap_means': bootstrap_means,
        'sample_size': len(genre_data)
    }


# TODO (Person 2): Implement additional helper functions as needed
# For example:
# - Function to run bootstrap for all genres in a region
# - Function to batch process multiple genre-region combinations
# - Function to save/load bootstrap results


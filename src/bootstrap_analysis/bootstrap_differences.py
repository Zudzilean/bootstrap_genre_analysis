"""
Bootstrap Functions for Difference Estimation

This module provides functions for bootstrap resampling to estimate
confidence intervals for pairwise differences between genres.

NOTE: This is a template framework for Person 2.
      Person 2 should:
      1. Review and test the provided implementations
      2. Verify statistical correctness of independent resampling
      3. Add error handling and edge cases
      4. Optimize if needed
      5. Complete any TODO items
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional


def bootstrap_difference(data_A: np.ndarray, 
                        data_B: np.ndarray, 
                        n_iterations: int = 10000, 
                        random_seed: Optional[int] = None) -> np.ndarray:
    """
    Bootstrap resampling for difference in means.
    
    For each bootstrap iteration:
    1. Resample from data_A with replacement (size n_A)
    2. Resample from data_B with replacement (size n_B)
    3. Compute difference: mean(A_bootstrap) - mean(B_bootstrap)
    
    IMPORTANT: Resampling must be done INDEPENDENTLY for each group.
    
    Args:
        data_A: 1D array for genre A
        data_B: 1D array for genre B
        n_iterations: Number of bootstrap iterations
        random_seed: Random seed for reproducibility
        
    Returns:
        Array of bootstrap differences (mean_A - mean_B)
    
    TODO (Person 2):
    - [ ] Add input validation (check if arrays are empty, etc.)
    - [ ] Verify that resampling is truly independent (current implementation looks correct)
    - [ ] Test with edge cases (one group has only 1 observation, etc.)
    - [ ] Consider performance optimization if needed
    """
    # TODO (Person 2): Add input validation
    # if len(data_A) == 0 or len(data_B) == 0:
    #     raise ValueError("Both data arrays must be non-empty")
    
    if random_seed is not None:
        np.random.seed(random_seed)
    
    n_A = len(data_A)
    n_B = len(data_B)
    bootstrap_differences = np.zeros(n_iterations)
    
    for i in range(n_iterations):
        # Resample independently from each group
        bootstrap_sample_A = np.random.choice(data_A, size=n_A, replace=True)
        bootstrap_sample_B = np.random.choice(data_B, size=n_B, replace=True)
        
        mean_A = np.mean(bootstrap_sample_A)
        mean_B = np.mean(bootstrap_sample_B)
        bootstrap_differences[i] = mean_A - mean_B
    
    return bootstrap_differences


def bootstrap_genre_difference(data: pd.DataFrame, 
                               genre_A: str, 
                               genre_B: str, 
                               region: str, 
                               n_iterations: int = 10000,
                               random_seed: Optional[int] = None) -> Dict:
    """
    Bootstrap difference between two genres in a region.
    
    Args:
        data: DataFrame with 'Genre' and 'log_sales' columns
        genre_A: First genre name
        genre_B: Second genre name
        region: Region name (for identification purposes)
        n_iterations: Number of bootstrap iterations
        random_seed: Random seed for reproducibility
        
    Returns:
        Dictionary with keys:
        - 'genre_A': First genre name
        - 'genre_B': Second genre name
        - 'region': Region name
        - 'mean_difference': Observed difference (mean_A - mean_B)
        - 'bootstrap_differences': Array of bootstrap differences
        - 'sample_size_A': Sample size for genre A
        - 'sample_size_B': Sample size for genre B
        - 'mean_A': Observed mean for genre A
        - 'mean_B': Observed mean for genre B
    """
    if 'Genre' not in data.columns or 'log_sales' not in data.columns:
        raise ValueError("DataFrame must contain 'Genre' and 'log_sales' columns")
    
    # Extract data for each genre
    data_A = data[data['Genre'] == genre_A]['log_sales'].values
    data_B = data[data['Genre'] == genre_B]['log_sales'].values
    
    if len(data_A) == 0:
        raise ValueError(f"No data found for genre: {genre_A}")
    if len(data_B) == 0:
        raise ValueError(f"No data found for genre: {genre_B}")
    
    # Calculate observed statistics
    mean_A = np.mean(data_A)
    mean_B = np.mean(data_B)
    observed_difference = mean_A - mean_B
    
    # Perform bootstrap
    bootstrap_differences = bootstrap_difference(
        data_A, data_B, n_iterations, random_seed
    )
    
    return {
        'genre_A': genre_A,
        'genre_B': genre_B,
        'region': region,
        'mean_difference': observed_difference,
        'bootstrap_differences': bootstrap_differences,
        'sample_size_A': len(data_A),
        'sample_size_B': len(data_B),
        'mean_A': mean_A,
        'mean_B': mean_B
    }


# TODO (Person 2): Implement additional helper functions as needed
# For example:
# - Function to generate all pairwise comparisons for a set of genres
# - Function to batch process multiple genre pairs across regions
# - Function to compare results with parametric tests (Welch's t-test) for validation


"""
Confidence Interval Calculation

This module provides functions for calculating confidence intervals
from bootstrap distributions and determining statistical significance.

NOTE: This is a template framework for Person 2.
      Person 2 should:
      1. Review and test the percentile method implementation
      2. Consider implementing BCa (Bias-Corrected and Accelerated) method as alternative
      3. Add error handling
      4. Complete any TODO items
"""

import numpy as np
from typing import Tuple


def percentile_ci(bootstrap_stats: np.ndarray, 
                 confidence_level: float = 0.95) -> Tuple[float, float]:
    """
    Calculate percentile-based confidence interval.
    
    Uses the percentile method: CI = [percentile_lower, percentile_upper]
    where percentiles are (1 - confidence_level) / 2 and 1 - (1 - confidence_level) / 2
    
    Args:
        bootstrap_stats: Array of bootstrap statistics (e.g., bootstrap means or differences)
        confidence_level: Confidence level (default: 0.95 for 95% CI)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    
    Raises:
        ValueError: If confidence_level is not in (0, 1) or bootstrap_stats is empty
    """
    # Input validation
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1")
    if len(bootstrap_stats) == 0:
        raise ValueError("bootstrap_stats array cannot be empty")
    
    alpha = 1 - confidence_level
    lower_bound = np.percentile(bootstrap_stats, 100 * (alpha / 2))
    upper_bound = np.percentile(bootstrap_stats, 100 * (1 - alpha / 2))
    
    return lower_bound, upper_bound


def is_significant(ci_lower: float, ci_upper: float, 
                  null_value: float = 0.0) -> bool:
    """
    Check if confidence interval excludes the null value (significant difference).
    
    For testing H0: difference = null_value vs H1: difference != null_value
    At significance level α = 0.05, reject H0 if null_value is not in the CI.
    
    Args:
        ci_lower: Lower bound of confidence interval
        ci_upper: Upper bound of confidence interval
        null_value: Null hypothesis value (default: 0.0 for testing no difference)
        
    Returns:
        True if CI excludes null_value (significant), False otherwise
    """
    return not (ci_lower <= null_value <= ci_upper)


# TODO (Person 2): Consider implementing additional helper functions
# For example:
# - Function to calculate BCa confidence interval (bias-corrected and accelerated)
# - Function to compare percentile CI with BCa CI
# - Function to calculate p-value from bootstrap distribution


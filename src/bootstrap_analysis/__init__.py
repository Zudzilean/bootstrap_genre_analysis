"""
Bootstrap Analysis Module

This module provides functions for bootstrap resampling and statistical analysis.
"""

from .bootstrap_means import (
    bootstrap_mean,
    bootstrap_genre_mean_by_region
)
from .bootstrap_differences import (
    bootstrap_difference,
    bootstrap_genre_difference
)
from .confidence_intervals import (
    percentile_ci,
    is_significant
)

__all__ = [
    'bootstrap_mean',
    'bootstrap_genre_mean_by_region',
    'bootstrap_difference',
    'bootstrap_genre_difference',
    'percentile_ci',
    'is_significant'
]

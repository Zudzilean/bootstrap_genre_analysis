"""
Visualization Module

This module provides functions for creating plots and figures.
"""

from .plot_bootstrap import (
    plot_bootstrap_distribution,
    plot_genre_means_by_region
)
from .plot_intervals import plot_confidence_intervals
from .plot_regional import (
    plot_regional_comparison,
    plot_difference_distributions
)

__all__ = [
    'plot_bootstrap_distribution',
    'plot_genre_means_by_region',
    'plot_confidence_intervals',
    'plot_regional_comparison',
    'plot_difference_distributions'
]


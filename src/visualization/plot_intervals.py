"""
Confidence Interval Plotting Functions

This module provides functions for visualizing confidence intervals.
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300


def plot_confidence_intervals(results: pd.DataFrame, 
                             save_path: Optional[str] = None,
                             title: Optional[str] = None) -> None:
    """
    Plot confidence intervals for genre means.
    
    Args:
        results: DataFrame with columns: genre, region (optional), mean, ci_lower, ci_upper
        save_path: Path to save figure
        title: Plot title (optional)
    
    Raises:
        ValueError: If required columns are missing or DataFrame is empty
    """
    # Input validation
    if results.empty:
        raise ValueError("results DataFrame cannot be empty")
    
    required_columns = ['genre', 'mean', 'ci_lower', 'ci_upper']
    missing = set(required_columns) - set(results.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create error bars for confidence intervals
    y_pos = range(len(results))
    
    # Plot means with error bars
    errors_lower = results['mean'] - results['ci_lower']
    errors_upper = results['ci_upper'] - results['mean']
    
    ax.errorbar(results['mean'], y_pos, 
               xerr=[errors_lower, errors_upper],
               fmt='o', capsize=5, capthick=2, markersize=8)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{row['genre']} ({row.get('region', 'N/A')})" 
                        for _, row in results.iterrows()])
    ax.set_xlabel('Mean Log Sales (95% CI)', fontsize=12)
    plot_title = title if title else 'Confidence Intervals for Genre Means'
    ax.set_title(plot_title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to: {save_path}")
    
    # Only show if not in non-interactive backend (e.g., during testing)
    if matplotlib.get_backend() != 'Agg':
        plt.show()
    else:
        plt.close()


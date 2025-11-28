"""
Bootstrap Distribution Plotting Functions

This module provides functions for visualizing bootstrap distributions.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Tuple, Dict, List
import pandas as pd

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300


def plot_bootstrap_distribution(bootstrap_stats: np.ndarray, 
                               true_statistic: Optional[float] = None,
                               ci_bounds: Optional[Tuple[float, float]] = None,
                               title: Optional[str] = None, 
                               save_path: Optional[str] = None,
                               xlabel: str = "Bootstrap Statistic") -> None:
    """
    Plot histogram of bootstrap distribution with CI and observed statistic.
    
    Args:
        bootstrap_stats: Array of bootstrap statistics
        true_statistic: True/observed statistic (optional, shown as vertical line)
        ci_bounds: Tuple of (lower, upper) CI bounds (optional, shown as shaded region)
        title: Plot title
        save_path: Path to save figure (optional)
        xlabel: Label for x-axis
    
    Raises:
        ValueError: If bootstrap_stats is empty or invalid
    """
    # Input validation
    if len(bootstrap_stats) == 0:
        raise ValueError("bootstrap_stats cannot be empty")
    if ci_bounds is not None and len(ci_bounds) != 2:
        raise ValueError("ci_bounds must be a tuple of (lower, upper)")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot histogram
    ax.hist(bootstrap_stats, bins=50, density=True, alpha=0.7, 
            color='steelblue', edgecolor='black')
    
    # Add observed statistic as vertical line
    if true_statistic is not None:
        ax.axvline(true_statistic, color='red', linestyle='--', 
                  linewidth=2, label=f'Observed: {true_statistic:.3f}')
    
    # Add confidence interval as shaded region
    if ci_bounds is not None:
        ci_lower, ci_upper = ci_bounds
        ax.axvspan(ci_lower, ci_upper, alpha=0.2, color='green', 
                  label=f'95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]')
        ax.axvline(ci_lower, color='green', linestyle=':', linewidth=1.5)
        ax.axvline(ci_upper, color='green', linestyle=':', linewidth=1.5)
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
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


def plot_genre_means_by_region(results: Dict[str, Dict], 
                               save_path: Optional[str] = None) -> None:
    """
    Plot bootstrap means for multiple genres across regions.
    
    Args:
        results: Dictionary of results keyed by (genre, region) tuple or string
                 Each value should be a dict with 'mean', 'bootstrap_means', etc.
        save_path: Path to save figure
    
    Raises:
        ValueError: If results is empty or missing required keys
    """
    # Input validation
    if not results:
        raise ValueError("results dictionary cannot be empty")
    
    # Convert results to DataFrame for easier plotting
    plot_data = []
    for key, result in results.items():
        if isinstance(key, tuple):
            genre, region = key
        else:
            genre = result.get('genre', 'Unknown')
            region = result.get('region', 'Unknown')
        
        plot_data.append({
            'Genre': genre,
            'Region': region,
            'Mean': result.get('mean', np.nan),
            'Sample_Size': result.get('sample_size', 0)
        })
    
    df = pd.DataFrame(plot_data)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Group by region for different subplots or grouped bars
    regions = df['Region'].unique()
    genres = df['Genre'].unique()
    
    x = np.arange(len(genres))
    width = 0.15
    
    for i, region in enumerate(regions):
        region_data = df[df['Region'] == region]
        means = [region_data[region_data['Genre'] == g]['Mean'].values[0] 
                if len(region_data[region_data['Genre'] == g]) > 0 else 0 
                for g in genres]
        offset = (i - len(regions) / 2) * width + width / 2
        ax.bar(x + offset, means, width, label=region)
    
    ax.set_xlabel('Genre', fontsize=12)
    ax.set_ylabel('Mean Log Sales', fontsize=12)
    ax.set_title('Genre Means by Region', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(genres, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
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


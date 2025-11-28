"""
Regional Comparison Plotting Functions

This module provides functions for creating regional comparison plots.
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Dict

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300


def plot_regional_comparison(results: Dict, 
                            save_path: Optional[str] = None,
                            title: Optional[str] = None) -> None:
    """
    Create heatmap showing genre performance across regions.
    
    Args:
        results: Dictionary of results with keys (genre, region) or dicts with 'genre'/'region'
                 Each value should have 'mean' key
        save_path: Path to save figure
        title: Plot title (optional)
    
    Raises:
        ValueError: If results is empty or missing required data
    """
    # Input validation
    if not results:
        raise ValueError("results dictionary cannot be empty")
    
    # Convert results to DataFrame format suitable for heatmap
    data_list = []
    for key, value in results.items():
        if isinstance(key, tuple):
            genre, region = key
        else:
            genre = value.get('genre', 'Unknown')
            region = value.get('region', 'Unknown')
        
        data_list.append({
            'Genre': genre,
            'Region': region,
            'Mean': value.get('mean', np.nan)
        })
    
    df = pd.DataFrame(data_list)
    pivot_df = df.pivot(index='Genre', columns='Region', values='Mean')
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(pivot_df, annot=True, fmt='.2f', cmap='YlOrRd', 
                cbar_kws={'label': 'Mean Log Sales'}, ax=ax)
    
    plot_title = title if title else 'Genre Performance Across Regions'
    ax.set_title(plot_title, fontsize=14, fontweight='bold')
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


def plot_difference_distributions(results: Dict, 
                                 save_path: Optional[str] = None,
                                 title: Optional[str] = None) -> None:
    """
    Plot bootstrap distributions of genre differences with zero reference.
    
    Args:
        results: Dictionary of difference results with 'bootstrap_differences' key
                 Each value should be a dict with 'bootstrap_differences', 'genre_A', 'genre_B', 'region' (optional)
        save_path: Path to save figure
        title: Plot title (optional)
    
    Raises:
        ValueError: If results is empty or missing bootstrap_differences
    """
    # Input validation
    if not results:
        raise ValueError("results dictionary cannot be empty")
    
    # Check if any result has bootstrap_differences
    has_differences = any('bootstrap_differences' in v for v in results.values() if isinstance(v, dict))
    if not has_differences:
        raise ValueError("No 'bootstrap_differences' found in results")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extract difference distributions
    for key, result in results.items():
        if 'bootstrap_differences' in result:
            label = f"{result.get('genre_A', 'A')} - {result.get('genre_B', 'B')}"
            if 'region' in result:
                label += f" ({result['region']})"
            
            ax.hist(result['bootstrap_differences'], bins=50, density=True, 
                   alpha=0.6, label=label)
    
    # Add zero reference line
    ax.axvline(0, color='red', linestyle='--', linewidth=2, 
              label='No Difference (H0)')
    
    ax.set_xlabel('Difference in Mean Log Sales', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    plot_title = title if title else 'Bootstrap Distributions of Genre Differences'
    ax.set_title(plot_title, fontsize=14, fontweight='bold')
    ax.legend()
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


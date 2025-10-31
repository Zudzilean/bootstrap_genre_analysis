"""
Regional Comparison Plotting Functions

This module provides functions for creating regional comparison plots.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Dict

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300


def plot_regional_comparison(results: Dict, 
                            save_path: Optional[str] = None) -> None:
    """
    Create heatmap or multi-panel plot showing genre performance across regions.
    
    Args:
        results: Dictionary of results (structure depends on implementation)
        save_path: Path to save figure
    """
    # Convert results to DataFrame format suitable for heatmap
    # This is a template - adapt based on actual results structure
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
    
    ax.set_title('Genre Performance Across Regions', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to: {save_path}")
    
    plt.show()


def plot_difference_distributions(results: Dict, 
                                 save_path: Optional[str] = None) -> None:
    """
    Plot bootstrap distributions of genre differences with zero reference.
    
    Args:
        results: Dictionary of difference results with 'bootstrap_differences' key
        save_path: Path to save figure
    """
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
    ax.set_title('Bootstrap Distributions of Genre Differences', 
                fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to: {save_path}")
    
    plt.show()


"""
Figure Generation Script

This script generates all required visualizations from bootstrap analysis results:
1. Bootstrap distribution plots for each genre-region combination
2. Confidence interval plots for genre means
3. Regional comparison heatmaps
4. Difference distribution plots with zero reference

Usage:
    From project root: python scripts/generate_figures.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.visualization.plot_bootstrap import (
    plot_bootstrap_distribution,
    plot_genre_means_by_region
)
from src.visualization.plot_intervals import plot_confidence_intervals
from src.visualization.plot_regional import (
    plot_regional_comparison,
    plot_difference_distributions
)
from src.bootstrap_analysis.bootstrap_means import bootstrap_genre_mean_by_region
from src.bootstrap_analysis.bootstrap_differences import bootstrap_genre_difference
from src.bootstrap_analysis.confidence_intervals import percentile_ci


def load_cleaned_data(region: str) -> pd.DataFrame:
    """Load cleaned data for a specific region."""
    filepath = PROJECT_ROOT / "data" / "processed" / f"cleaned_data_{region.lower()}_1995-2016.csv"
    return pd.read_csv(filepath)


def load_bootstrap_results():
    """Load bootstrap analysis results."""
    means_path = PROJECT_ROOT / "results" / "tables" / "bootstrap_means_all_regions.csv"
    diff_path = PROJECT_ROOT / "results" / "tables" / "bootstrap_differences_all_regions.csv"
    
    means_df = pd.read_csv(means_path)
    diff_df = pd.read_csv(diff_path)
    
    return means_df, diff_df


def generate_bootstrap_distributions():
    """Generate bootstrap distribution plots for each genre-region combination."""
    print("=" * 60)
    print("Generating Bootstrap Distribution Plots")
    print("=" * 60)
    
    regions = ['Global', 'NA', 'EU', 'JP', 'Other']
    genres = ['Action', 'Role-Playing', 'Simulation']
    n_iterations = 10000
    random_seed = 42
    
    for region in regions:
        print(f"\nProcessing region: {region}")
        data = load_cleaned_data(region)
        
        for genre in genres:
            print(f"  Generating plot for {genre}...", end=" ")
            try:
                # Run bootstrap to get distribution
                result = bootstrap_genre_mean_by_region(
                    data,
                    genre=genre,
                    region=region,
                    n_iterations=n_iterations,
                    random_seed=random_seed
                )
                
                # Calculate CI
                ci_lower, ci_upper = percentile_ci(result['bootstrap_means'], confidence_level=0.95)
                
                # Generate plot
                save_path = PROJECT_ROOT / "results" / "figures" / f"bootstrap_dist_{genre.lower()}_{region.lower()}.png"
                plot_bootstrap_distribution(
                    bootstrap_stats=result['bootstrap_means'],
                    true_statistic=result['mean'],
                    ci_bounds=(ci_lower, ci_upper),
                    title=f"Bootstrap Distribution: {genre} in {region}",
                    xlabel="Mean Log Sales",
                    save_path=str(save_path)
                )
                print("✓")
                
            except Exception as e:
                print(f"✗ Error: {e}")


def generate_confidence_intervals():
    """Generate confidence interval plots."""
    print("\n" + "=" * 60)
    print("Generating Confidence Interval Plots")
    print("=" * 60)
    
    means_df, _ = load_bootstrap_results()
    
    # Plot for each region
    regions = means_df['Region'].unique()
    
    for region in regions:
        print(f"  Generating CI plot for {region}...", end=" ")
        region_data = means_df[means_df['Region'] == region].copy()
        
        # Rename columns to match expected format
        region_data = region_data.rename(columns={
            'Genre': 'genre',
            'Region': 'region',
            'Mean': 'mean',
            'CI_Lower': 'ci_lower',
            'CI_Upper': 'ci_upper'
        })
        
        save_path = PROJECT_ROOT / "results" / "figures" / f"confidence_intervals_{region.lower()}.png"
        plot_confidence_intervals(
            results=region_data,
            save_path=str(save_path),
            title=f"95% Confidence Intervals: Genre Means in {region}"
        )
        print("✓")
    
    # Combined plot for all regions
    print("  Generating combined CI plot...", end=" ")
    combined_data = means_df.copy()
    combined_data = combined_data.rename(columns={
        'Genre': 'genre',
        'Region': 'region',
        'Mean': 'mean',
        'CI_Lower': 'ci_lower',
        'CI_Upper': 'ci_upper'
    })
    
    save_path = PROJECT_ROOT / "results" / "figures" / "confidence_intervals_all_regions.png"
    plot_confidence_intervals(
        results=combined_data,
        save_path=str(save_path),
        title="95% Confidence Intervals: Genre Means Across All Regions"
    )
    print("✓")


def generate_regional_comparison():
    """Generate regional comparison heatmap."""
    print("\n" + "=" * 60)
    print("Generating Regional Comparison Heatmap")
    print("=" * 60)
    
    means_df, _ = load_bootstrap_results()
    
    # Convert to dictionary format for plotting
    results_dict = {}
    for _, row in means_df.iterrows():
        key = (row['Genre'], row['Region'])
        results_dict[key] = {
            'genre': row['Genre'],
            'region': row['Region'],
            'mean': row['Mean']
        }
    
    print("  Generating heatmap...", end=" ")
    save_path = PROJECT_ROOT / "results" / "figures" / "regional_comparison_heatmap.png"
    plot_regional_comparison(
        results=results_dict,
        save_path=str(save_path),
        title="Genre Performance Across Regions"
    )
    print("✓")


def generate_genre_means_comparison():
    """Generate genre means comparison bar chart."""
    print("\n" + "=" * 60)
    print("Generating Genre Means Comparison")
    print("=" * 60)
    
    means_df, _ = load_bootstrap_results()
    
    # Convert to dictionary format
    results_dict = {}
    for _, row in means_df.iterrows():
        key = (row['Genre'], row['Region'])
        results_dict[key] = {
            'genre': row['Genre'],
            'region': row['Region'],
            'mean': row['Mean'],
            'sample_size': row['Sample_Size']
        }
    
    print("  Generating bar chart...", end=" ")
    save_path = PROJECT_ROOT / "results" / "figures" / "genre_means_by_region.png"
    plot_genre_means_by_region(
        results=results_dict,
        save_path=str(save_path)
    )
    print("✓")


def generate_difference_distributions():
    """Generate difference distribution plots."""
    print("\n" + "=" * 60)
    print("Generating Difference Distribution Plots")
    print("=" * 60)
    
    regions = ['Global', 'NA', 'EU', 'JP', 'Other']
    genre_pairs = [
        ('Action', 'Role-Playing'),
        ('Action', 'Simulation'),
        ('Role-Playing', 'Simulation')
    ]
    n_iterations = 10000
    random_seed = 42
    
    # Generate plot for each region
    for region in regions:
        print(f"\nProcessing region: {region}")
        data = load_cleaned_data(region)
        
        results_dict = {}
        for genre_A, genre_B in genre_pairs:
            print(f"  Generating plot for {genre_A} vs {genre_B}...", end=" ")
            try:
                result = bootstrap_genre_difference(
                    data,
                    genre_A=genre_A,
                    genre_B=genre_B,
                    region=region,
                    n_iterations=n_iterations,
                    random_seed=random_seed
                )
                
                key = f"{genre_A}_{genre_B}_{region}"
                results_dict[key] = {
                    'genre_A': genre_A,
                    'genre_B': genre_B,
                    'region': region,
                    'bootstrap_differences': result['bootstrap_differences']
                }
                print("✓")
                
            except Exception as e:
                print(f"✗ Error: {e}")
        
        # Generate combined plot for this region
        if results_dict:
            print(f"  Generating combined plot for {region}...", end=" ")
            save_path = PROJECT_ROOT / "results" / "figures" / f"difference_distributions_{region.lower()}.png"
            plot_difference_distributions(
                results=results_dict,
                save_path=str(save_path),
                title=f"Bootstrap Distributions of Genre Differences: {region}"
            )
            print("✓")


def main():
    """Generate all required figures."""
    import os
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    
    original_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)
    
    try:
        print("\n" + "=" * 60)
        print("Figure Generation Pipeline")
        print("=" * 60)
        
        # Ensure output directory exists
        (PROJECT_ROOT / "results" / "figures").mkdir(parents=True, exist_ok=True)
        
        # Generate all figures
        generate_bootstrap_distributions()
        generate_confidence_intervals()
        generate_regional_comparison()
        generate_genre_means_comparison()
        generate_difference_distributions()
        
        print("\n" + "=" * 60)
        print("Figure Generation Complete!")
        print("=" * 60)
        print(f"\nAll figures saved to: results/figures/")
        print("\nGenerated figures:")
        figures_dir = PROJECT_ROOT / "results" / "figures"
        figure_files = sorted(figures_dir.glob("*.png"))
        for fig_file in figure_files:
            print(f"  - {fig_file.name}")
        
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()


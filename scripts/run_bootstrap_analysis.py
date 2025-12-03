"""
Bootstrap Analysis Pipeline Script

This script runs the complete bootstrap analysis:
1. Load cleaned data for each region
2. Run bootstrap for genre means (all genres × all regions)
3. Run bootstrap for genre differences (all pairs × all regions)
4. Calculate 95% confidence intervals and significance tests
5. Save results to results/tables/

Usage:
    From project root: python scripts/run_bootstrap_analysis.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from itertools import combinations

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.bootstrap_analysis.bootstrap_means import bootstrap_genre_mean_by_region
from src.bootstrap_analysis.bootstrap_differences import bootstrap_genre_difference
from src.bootstrap_analysis.confidence_intervals import percentile_ci, is_significant
from src.reporting.generate_tables import create_summary_table, export_results_table


def load_cleaned_data(region: str) -> pd.DataFrame:
    """Load cleaned data for a specific region."""
    filepath = PROJECT_ROOT / "data" / "processed" / f"cleaned_data_{region.lower()}_1995-2016.csv"
    if not filepath.exists():
        raise FileNotFoundError(f"Cleaned data file not found: {filepath}")
    return pd.read_csv(filepath)


def run_bootstrap_means_analysis():
    """Run bootstrap analysis for genre means across all regions."""
    print("=" * 60)
    print("Bootstrap Analysis: Genre Means")
    print("=" * 60)
    
    regions = ['Global', 'NA', 'EU', 'JP', 'Other']
    genres = ['Action', 'Role-Playing', 'Simulation']
    n_iterations = 10000
    random_seed = 42
    
    all_results = []
    
    for region in regions:
        print(f"\nProcessing region: {region}")
        try:
            data = load_cleaned_data(region)
            print(f"  Loaded {len(data)} rows")
            
            for genre in genres:
                print(f"  Analyzing {genre}...", end=" ")
                try:
                    # Run bootstrap
                    result = bootstrap_genre_mean_by_region(
                        data, 
                        genre=genre, 
                        region=region,
                        n_iterations=n_iterations,
                        random_seed=random_seed
                    )
                    
                    # Calculate confidence interval
                    ci_lower, ci_upper = percentile_ci(
                        result['bootstrap_means'], 
                        confidence_level=0.95
                    )
                    
                    # Store results
                    all_results.append({
                        'genre': genre,
                        'region': region,
                        'mean': result['mean'],
                        'ci_lower': ci_lower,
                        'ci_upper': ci_upper,
                        'sample_size': result['sample_size']
                    })
                    
                    print(f"✓ (n={result['sample_size']}, mean={result['mean']:.3f})")
                    
                except ValueError as e:
                    print(f"✗ Error: {e}")
                    continue
                    
        except FileNotFoundError as e:
            print(f"  ✗ {e}")
            continue
    
    # Save results
    if all_results:
        df = create_summary_table(all_results, decimals=3, sort_results=True)
        output_path = PROJECT_ROOT / "results" / "tables" / "bootstrap_means_all_regions.csv"
        export_results_table(df, str(output_path))
        print(f"\n✓ Saved {len(all_results)} results to {output_path}")
    
    return all_results


def run_bootstrap_differences_analysis():
    """Run bootstrap analysis for genre differences across all regions."""
    print("\n" + "=" * 60)
    print("Bootstrap Analysis: Genre Differences")
    print("=" * 60)
    
    regions = ['Global', 'NA', 'EU', 'JP', 'Other']
    genres = ['Action', 'Role-Playing', 'Simulation']
    n_iterations = 10000
    random_seed = 42
    
    # Generate all pairs
    genre_pairs = list(combinations(genres, 2))
    
    all_results = []
    
    for region in regions:
        print(f"\nProcessing region: {region}")
        try:
            data = load_cleaned_data(region)
            print(f"  Loaded {len(data)} rows")
            
            for genre_A, genre_B in genre_pairs:
                print(f"  Analyzing {genre_A} vs {genre_B}...", end=" ")
                try:
                    # Run bootstrap difference
                    result = bootstrap_genre_difference(
                        data,
                        genre_A=genre_A,
                        genre_B=genre_B,
                        region=region,
                        n_iterations=n_iterations,
                        random_seed=random_seed
                    )
                    
                    # Calculate confidence interval
                    ci_lower, ci_upper = percentile_ci(
                        result['bootstrap_differences'],
                        confidence_level=0.95
                    )
                    
                    # Test significance
                    significant = is_significant(ci_lower, ci_upper, null_value=0.0)
                    
                    # Store results
                    all_results.append({
                        'genre_A': genre_A,
                        'genre_B': genre_B,
                        'region': region,
                        'mean_difference': result['mean_difference'],
                        'ci_lower': ci_lower,
                        'ci_upper': ci_upper,
                        'significant': significant,
                        'sample_size_A': result['sample_size_A'],
                        'sample_size_B': result['sample_size_B']
                    })
                    
                    sig_marker = "***" if significant else ""
                    print(f"✓ (diff={result['mean_difference']:.3f} {sig_marker})")
                    
                except ValueError as e:
                    print(f"✗ Error: {e}")
                    continue
                    
        except FileNotFoundError as e:
            print(f"  ✗ {e}")
            continue
    
    # Save results
    if all_results:
        df = create_summary_table(all_results, decimals=3, sort_results=True)
        output_path = PROJECT_ROOT / "results" / "tables" / "bootstrap_differences_all_regions.csv"
        export_results_table(df, str(output_path))
        print(f"\n✓ Saved {len(all_results)} results to {output_path}")
    
    return all_results


def save_results_by_region(means_results, diff_results):
    """Save results separated by region."""
    print("\n" + "=" * 60)
    print("Saving Results by Region")
    print("=" * 60)
    
    regions = ['Global', 'NA', 'EU', 'JP', 'Other']
    
    for region in regions:
        # Filter means results for this region
        region_means = [r for r in means_results if r['region'] == region]
        if region_means:
            df_means = create_summary_table(region_means, decimals=3, sort_results=True)
            output_path = PROJECT_ROOT / "results" / "tables" / f"bootstrap_means_{region.lower()}.csv"
            export_results_table(df_means, str(output_path))
            print(f"✓ Saved means for {region}: {len(region_means)} results")
        
        # Filter difference results for this region
        region_diffs = [r for r in diff_results if r['region'] == region]
        if region_diffs:
            df_diffs = create_summary_table(region_diffs, decimals=3, sort_results=True)
            output_path = PROJECT_ROOT / "results" / "tables" / f"bootstrap_differences_{region.lower()}.csv"
            export_results_table(df_diffs, str(output_path))
            print(f"✓ Saved differences for {region}: {len(region_diffs)} results")


def main():
    """Run the complete bootstrap analysis pipeline."""
    import os
    original_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)
    
    try:
        print("\n" + "=" * 60)
        print("Bootstrap Analysis Pipeline")
        print("=" * 60)
        print(f"Bootstrap iterations: 10,000")
        print(f"Confidence level: 95%")
        print(f"Random seed: 42")
        print(f"Genres: Action, Role-Playing, Simulation")
        print(f"Regions: Global, NA, EU, JP, Other")
        
        # Run bootstrap for means
        means_results = run_bootstrap_means_analysis()
        
        # Run bootstrap for differences
        diff_results = run_bootstrap_differences_analysis()
        
        # Save results by region
        save_results_by_region(means_results, diff_results)
        
        print("\n" + "=" * 60)
        print("Bootstrap Analysis Complete!")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  - Genre means analyzed: {len(means_results)}")
        print(f"  - Genre differences analyzed: {len(diff_results)}")
        print(f"  - Results saved to: results/tables/")
        print("\nNext steps:")
        print("  1. Review results in results/tables/")
        print("  2. Generate visualizations using scripts/generate_figures.py")
        print("  3. Create Jupyter Notebook for complete workflow")
        
        return means_results, diff_results
    
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()


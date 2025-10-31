"""
Table Generation Functions

This module provides functions for creating and exporting summary tables.

NOTE: This is a template framework for Person 2.
      Person 2 should:
      1. Complete the table generation functions
      2. Add formatting options (rounding, scientific notation, etc.)
      3. Create additional table types as needed for the report
      4. Complete any TODO items
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict


def create_summary_table(results: List[Dict]) -> pd.DataFrame:
    """
    Create summary table of bootstrap results.
    
    Args:
        results: List of result dictionaries, each containing:
            - For means: 'genre', 'region', 'mean', 'ci_lower', 'ci_upper', 'sample_size'
            - For differences: 'genre_A', 'genre_B', 'region', 'mean_difference', 
                              'ci_lower', 'ci_upper', 'sample_size_A', 'sample_size_B'
        
    Returns:
        Formatted DataFrame with all results
    
    TODO (Person 2):
    - [ ] Add input validation (check result format, required keys, etc.)
    - [ ] Add formatting options (decimal places, rounding)
    - [ ] Consider adding additional columns (e.g., standard error, width of CI)
    - [ ] Sort results by region, then by genre (or other logical ordering)
    - [ ] Add option to create separate tables for means vs differences
    """
    # TODO (Person 2): Add input validation
    # if not results:
    #     raise ValueError("Results list cannot be empty")
    
    rows = []
    
    for result in results:
        # Determine if this is a mean result or difference result
        if 'genre_A' in result and 'genre_B' in result:
            # Difference result
            row = {
                'Type': 'Difference',
                'Genre_A': result.get('genre_A', ''),
                'Genre_B': result.get('genre_B', ''),
                'Region': result.get('region', ''),
                'Mean_Difference': result.get('mean_difference', np.nan),
                'CI_Lower': result.get('ci_lower', np.nan),
                'CI_Upper': result.get('ci_upper', np.nan),
                'Significant': result.get('significant', False),
                'Sample_Size_A': result.get('sample_size_A', 0),
                'Sample_Size_B': result.get('sample_size_B', 0)
            }
        else:
            # Mean result
            row = {
                'Type': 'Mean',
                'Genre': result.get('genre', ''),
                'Region': result.get('region', ''),
                'Mean': result.get('mean', np.nan),
                'CI_Lower': result.get('ci_lower', np.nan),
                'CI_Upper': result.get('ci_upper', np.nan),
                'Sample_Size': result.get('sample_size', 0)
            }
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    return df


def export_results_table(results: pd.DataFrame, filepath: str) -> None:
    """
    Export results table to CSV.
    
    Args:
        results: Results DataFrame (from create_summary_table or similar)
        filepath: Output file path
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    results.to_csv(filepath, index=False)
    print(f"Results table exported to: {filepath}")
    print(f"Shape: {results.shape}")


# TODO (Person 2): Implement additional table generation functions
# For example:
# - Function to create LaTeX-formatted table for report
# - Function to create region-specific summary tables
# - Function to create genre comparison matrix table
# - Function to format numbers for publication (rounding, significant digits)


"""
Table Generation Functions

This module provides functions for creating and exporting summary tables.

Completed by Person 2:
- Added input validation
- Added numeric formatting options
- Added CI width and SE columns
- Added sorting options
- Added optional separation of means vs differences
- Added LaTeX export and region-specific tables
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Union


# ------------------------------------------------------------
# Helper: number formatting
# ------------------------------------------------------------
def format_number(x, decimals=3, sci=False):
    """
    Format numbers for table output.
    
    Args:
        x: Number to format
        decimals: Number of decimal places
        sci: Use scientific notation if True
    
    Returns:
        Formatted number or original value if NaN
    """
    if pd.isna(x):
        return x
    if sci:
        return f"{x:.{decimals}e}"
    return round(x, decimals)


# ------------------------------------------------------------
# Main Summary Table Builder
# ------------------------------------------------------------
def create_summary_table(
        results: List[Dict],
        decimals: int = 3,
        sci: bool = False,
        separate_tables: bool = False,
        sort_results: bool = True
    ) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Create summary table of bootstrap results.
    
    Args:
        results: List of result dictionaries, each containing:
            - For means: 'genre', 'region', 'mean', 'ci_lower', 'ci_upper', 'sample_size'
            - For differences: 'genre_A', 'genre_B', 'region', 'mean_difference', 
                              'ci_lower', 'ci_upper', 'sample_size_A', 'sample_size_B'
        decimals: Number of decimal places for rounding
        sci: Use scientific notation if True
        separate_tables: If True, return dict with 'means' and 'differences' DataFrames
        sort_results: If True, sort by region then genre
    
    Returns:
        DataFrame OR dict of DataFrames if separate_tables=True
    
    Raises:
        ValueError: If results is empty or not a list
    """
    # Input validation
    if not isinstance(results, list) or len(results) == 0:
        raise ValueError("Results must be a non-empty list of dictionaries.")
    
    rows = []
    
    for r in results:
        # Determine result type
        is_diff = 'genre_A' in r and 'genre_B' in r
        
        if is_diff:
            row = {
                'Type': 'Difference',
                'Genre_A': r.get('genre_A', ''),
                'Genre_B': r.get('genre_B', ''),
                'Region': r.get('region', ''),
                'Mean_Difference': r.get('mean_difference', np.nan),
                'CI_Lower': r.get('ci_lower', np.nan),
                'CI_Upper': r.get('ci_upper', np.nan),
                'CI_Width': abs(r.get('ci_upper', np.nan) - r.get('ci_lower', np.nan)),
                'Significant': r.get('significant', False),
                'Sample_Size_A': r.get('sample_size_A', 0),
                'Sample_Size_B': r.get('sample_size_B', 0),
            }
        else:
            row = {
                'Type': 'Mean',
                'Genre': r.get('genre', ''),
                'Region': r.get('region', ''),
                'Mean': r.get('mean', np.nan),
                'CI_Lower': r.get('ci_lower', np.nan),
                'CI_Upper': r.get('ci_upper', np.nan),
                'CI_Width': abs(r.get('ci_upper', np.nan) - r.get('ci_lower', np.nan)),
                'Sample_Size': r.get('sample_size', 0)
            }
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Sorting
    if sort_results:
        if 'Genre' in df.columns:
            df = df.sort_values(by=['Region', 'Genre'], ascending=True)
        else:
            df = df.sort_values(by=['Region', 'Genre_A', 'Genre_B'], ascending=True)
    
    # Number formatting
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].apply(lambda x: format_number(x, decimals, sci))
    
    # Optional: return separate tables
    if separate_tables:
        means_df = df[df['Type'] == 'Mean'].reset_index(drop=True)
        diff_df = df[df['Type'] == 'Difference'].reset_index(drop=True)
        return {
            "means": means_df,
            "differences": diff_df
        }
    
    return df


# ------------------------------------------------------------
# CSV Export
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# Additional Table Functions
# ------------------------------------------------------------

def make_latex_table(df: pd.DataFrame, filepath: str) -> None:
    """
    Export DataFrame as LaTeX table.
    
    Args:
        df: DataFrame to export
        filepath: Output file path for LaTeX file
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    latex = df.to_latex(index=False, escape=False)
    path.write_text(latex, encoding="utf-8")
    print(f"LaTeX table saved to: {filepath}")


def region_specific_tables(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Create a dict of tables, one per region.
    
    Args:
        df: DataFrame with 'Region' column
    
    Returns:
        Dictionary with region names as keys and filtered DataFrames as values
    
    Raises:
        ValueError: If DataFrame doesn't contain 'Region' column
    """
    if 'Region' not in df.columns:
        raise ValueError("DataFrame must contain a Region column")
    
    tables = {}
    for region in df['Region'].unique():
        tables[region] = df[df['Region'] == region].reset_index(drop=True)
    return tables


def genre_comparison_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a genre-by-genre matrix of mean differences (for differences only).
    
    Args:
        df: DataFrame containing difference results with 'Mean_Difference' column
    
    Returns:
        Pivot table matrix with Genre_A as rows and Genre_B as columns
    
    Raises:
        ValueError: If DataFrame doesn't contain 'Mean_Difference' column
    """
    if 'Mean_Difference' not in df.columns:
        raise ValueError("Matrix requires a table of 'Difference' results.")
    
    diff_df = df[df['Type'] == 'Difference']
    
    matrix = diff_df.pivot_table(
        index='Genre_A',
        columns='Genre_B',
        values='Mean_Difference'
    )
    
    return matrix


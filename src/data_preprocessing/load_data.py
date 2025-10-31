"""
Data Loading Functions

This module provides functions for loading raw video game sales data
from CSV files and validating data integrity.
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, List


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Load raw video game sales data from CSV file.
    
    Args:
        filepath: Path to vgsales.csv file
        
    Returns:
        DataFrame with raw data
        
    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file format is invalid
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")


def validate_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate data integrity and completeness.
    
    Checks for:
    - Required columns presence
    - Data types
    - Missing values in critical columns
    - Negative sales values
    
    Args:
        df: Input DataFrame
        
    Returns:
        Tuple of (is_valid, list_of_issues)
        is_valid: True if data passes all checks
        list_of_issues: List of validation issue descriptions
    """
    issues = []
    required_columns = [
        'Name', 'Platform', 'Year', 'Genre', 'Publisher',
        'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'
    ]
    
    # Check required columns
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        issues.append(f"Missing required columns: {missing_columns}")
    
    # Check for missing Genre (critical for analysis)
    if 'Genre' in df.columns:
        missing_genre = df['Genre'].isna().sum()
        if missing_genre > 0:
            issues.append(f"Found {missing_genre} rows with missing Genre")
    
    # Check for invalid sales values (should be non-negative)
    sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
    for col in sales_columns:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                issues.append(f"Found {negative_count} rows with negative {col}")
    
    is_valid = len(issues) == 0
    return is_valid, issues


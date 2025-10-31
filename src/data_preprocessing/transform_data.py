"""
Data Transformation Functions

This module provides functions for transforming video game sales data,
including log transformations and data reshaping for analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Literal


def apply_log_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply log1p transformation to all sales columns.
    
    Creates new columns:
    - log_sales_global: log1p(Global_Sales)
    - log_sales_na: log1p(NA_Sales)
    - log_sales_eu: log1p(EU_Sales)
    - log_sales_jp: log1p(JP_Sales)
    - log_sales_other: log1p(Other_Sales)
    
    Args:
        df: Input DataFrame with sales columns
        
    Returns:
        DataFrame with log-transformed columns added
    """
    df_transformed = df.copy()
    
    # Mapping of original columns to log-transformed column names
    sales_mapping = {
        'Global_Sales': 'log_sales_global',
        'NA_Sales': 'log_sales_na',
        'EU_Sales': 'log_sales_eu',
        'JP_Sales': 'log_sales_jp',
        'Other_Sales': 'log_sales_other'
    }
    
    for original_col, log_col in sales_mapping.items():
        if original_col in df_transformed.columns:
            df_transformed[log_col] = np.log1p(df_transformed[original_col])
        else:
            print(f"Warning: Column {original_col} not found, skipping log transformation")
    
    return df_transformed


def reshape_for_analysis(df: pd.DataFrame, 
                        region: Literal['Global', 'NA', 'EU', 'JP', 'Other']) -> pd.DataFrame:
    """
    Reshape data for bootstrap analysis by region.
    
    Args:
        df: DataFrame with log-transformed sales columns
        region: One of ['Global', 'NA', 'EU', 'JP', 'Other']
        
    Returns:
        DataFrame with columns: Genre, log_sales, (optional: Year, Platform)
        
    Raises:
        ValueError: If region is invalid or required columns are missing
    """
    region_mapping = {
        'Global': 'log_sales_global',
        'NA': 'log_sales_na',
        'EU': 'log_sales_eu',
        'JP': 'log_sales_jp',
        'Other': 'log_sales_other'
    }
    
    if region not in region_mapping:
        raise ValueError(f"Invalid region: {region}. Must be one of {list(region_mapping.keys())}")
    
    log_col = region_mapping[region]
    
    if log_col not in df.columns:
        raise ValueError(f"Log-transformed column {log_col} not found. Run apply_log_transform() first.")
    
    if 'Genre' not in df.columns:
        raise ValueError("Genre column not found in DataFrame")
    
    # Select relevant columns
    columns_to_keep = ['Genre', log_col]
    if 'Year' in df.columns:
        columns_to_keep.append('Year')
    if 'Platform' in df.columns:
        columns_to_keep.append('Platform')
    
    df_reshaped = df[columns_to_keep].copy()
    
    # Rename log_sales column to standardized 'log_sales'
    df_reshaped = df_reshaped.rename(columns={log_col: 'log_sales'})
    
    # Remove any rows with missing log_sales (shouldn't happen, but safety check)
    df_reshaped = df_reshaped.dropna(subset=['log_sales'])
    
    return df_reshaped


def save_cleaned_data(df: pd.DataFrame, 
                     region: str, 
                     time_window: str = 'all',
                     output_dir: str = 'data/processed') -> str:
    """
    Save cleaned data to CSV file.
    
    Args:
        df: Cleaned DataFrame
        region: Region name (e.g., 'Global', 'NA', 'EU', 'JP', 'Other')
        time_window: Time window description (e.g., 'all', '1995-2016')
        output_dir: Output directory path
        
    Returns:
        Path to saved file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filename = f"cleaned_data_{region.lower()}_{time_window}.csv"
    filepath = output_path / filename
    
    df.to_csv(filepath, index=False)
    print(f"Saved cleaned data to: {filepath}")
    print(f"Shape: {df.shape}, Columns: {list(df.columns)}")
    
    return str(filepath)


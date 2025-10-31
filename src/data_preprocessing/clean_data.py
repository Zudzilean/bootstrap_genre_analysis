"""
Data Cleaning Functions

This module provides functions for cleaning and filtering video game sales data.
"""

import pandas as pd
import numpy as np
from typing import List, Optional


def remove_invalid_entries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with missing Genre, invalid Year, or zero/negative Global_Sales.
    
    Filtering criteria:
    - Drop rows where Genre is missing
    - Drop rows where Year is missing or non-numeric
    - Drop rows where Global_Sales <= 0
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    df_clean = df.copy()
    
    # Remove rows with missing Genre
    initial_count = len(df_clean)
    df_clean = df_clean.dropna(subset=['Genre'])
    
    # Remove rows with invalid Year (non-numeric or missing)
    if 'Year' in df_clean.columns:
        df_clean['Year'] = pd.to_numeric(df_clean['Year'], errors='coerce')
        df_clean = df_clean.dropna(subset=['Year'])
    
    # Remove rows with zero or negative Global_Sales
    if 'Global_Sales' in df_clean.columns:
        df_clean = df_clean[df_clean['Global_Sales'] > 0]
    
    removed_count = initial_count - len(df_clean)
    if removed_count > 0:
        print(f"Removed {removed_count} invalid entries ({initial_count} -> {len(df_clean)})")
    
    return df_clean


def filter_time_window(df: pd.DataFrame, 
                      start_year: Optional[int] = None, 
                      end_year: Optional[int] = None) -> pd.DataFrame:
    """
    Filter data by release year range.
    
    Args:
        df: Input DataFrame
        start_year: Start year (inclusive). If None, no lower bound.
        end_year: End year (inclusive). If None, no upper bound.
        
    Returns:
        Filtered DataFrame
    """
    df_filtered = df.copy()
    
    if 'Year' not in df_filtered.columns:
        print("Warning: Year column not found, skipping time window filter")
        return df_filtered
    
    if start_year is not None:
        df_filtered = df_filtered[df_filtered['Year'] >= start_year]
    
    if end_year is not None:
        df_filtered = df_filtered[df_filtered['Year'] <= end_year]
    
    return df_filtered


def select_genres(df: pd.DataFrame, genres: List[str]) -> pd.DataFrame:
    """
    Filter data to include only specified genres.
    
    Args:
        df: Input DataFrame
        genres: List of genre names to include (case-sensitive)
        
    Returns:
        Filtered DataFrame containing only specified genres
    """
    if 'Genre' not in df.columns:
        raise ValueError("Genre column not found in DataFrame")
    
    available_genres = df['Genre'].unique().tolist()
    invalid_genres = set(genres) - set(available_genres)
    
    if invalid_genres:
        print(f"Warning: The following genres are not in the data: {invalid_genres}")
        print(f"Available genres: {available_genres}")
    
    valid_genres = [g for g in genres if g in available_genres]
    df_filtered = df[df['Genre'].isin(valid_genres)].copy()
    
    return df_filtered


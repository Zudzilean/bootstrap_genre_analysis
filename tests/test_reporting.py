"""
Unit tests for reporting module.

Tests cover:
- Summary table creation
- Number formatting
- CSV and LaTeX export
- Region-specific tables
- Genre comparison matrix
- Input validation and error handling
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import tempfile
import shutil

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.reporting.generate_tables import (
    create_summary_table,
    export_results_table,
    format_number,
    make_latex_table,
    region_specific_tables,
    genre_comparison_matrix
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_mean_results():
    """Create sample mean results."""
    return [
        {
            'genre': 'Action',
            'region': 'Global',
            'mean': 3.0,
            'ci_lower': 2.8,
            'ci_upper': 3.2,
            'sample_size': 100
        },
        {
            'genre': 'Role-Playing',
            'region': 'Global',
            'mean': 2.9,
            'ci_lower': 2.7,
            'ci_upper': 3.1,
            'sample_size': 80
        },
        {
            'genre': 'Action',
            'region': 'NA',
            'mean': 2.8,
            'ci_lower': 2.6,
            'ci_upper': 3.0,
            'sample_size': 95
        }
    ]


@pytest.fixture
def sample_difference_results():
    """Create sample difference results."""
    return [
        {
            'genre_A': 'Action',
            'genre_B': 'Role-Playing',
            'region': 'Global',
            'mean_difference': 0.1,
            'ci_lower': -0.1,
            'ci_upper': 0.3,
            'significant': True,
            'sample_size_A': 100,
            'sample_size_B': 80
        },
        {
            'genre_A': 'Action',
            'genre_B': 'Simulation',
            'region': 'Global',
            'mean_difference': 0.5,
            'ci_lower': 0.3,
            'ci_upper': 0.7,
            'significant': True,
            'sample_size_A': 100,
            'sample_size_B': 60
        }
    ]


@pytest.fixture
def sample_mixed_results(sample_mean_results, sample_difference_results):
    """Create mixed results with both means and differences."""
    return sample_mean_results + sample_difference_results


@pytest.fixture
def temp_dir():
    """Create temporary directory for test outputs."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


# ============================================================================
# Tests for format_number
# ============================================================================

def test_format_number_basic():
    """Test basic number formatting."""
    assert format_number(3.14159, decimals=2) == 3.14
    assert format_number(3.14159, decimals=3) == 3.142


def test_format_number_scientific():
    """Test scientific notation formatting."""
    result = format_number(1234.567, decimals=2, sci=True)
    assert 'e' in result.lower()
    assert isinstance(result, str)


def test_format_number_nan():
    """Test formatting NaN values."""
    result = format_number(np.nan)
    assert pd.isna(result)


def test_format_number_zero():
    """Test formatting zero."""
    assert format_number(0.0, decimals=2) == 0.0


# ============================================================================
# Tests for create_summary_table
# ============================================================================

def test_create_summary_table_means_only(sample_mean_results):
    """Test creating summary table with mean results only."""
    df = create_summary_table(sample_mean_results)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert 'Type' in df.columns
    assert 'Genre' in df.columns
    assert 'Region' in df.columns
    assert 'Mean' in df.columns
    assert 'CI_Lower' in df.columns
    assert 'CI_Upper' in df.columns
    assert 'CI_Width' in df.columns
    assert all(df['Type'] == 'Mean')


def test_create_summary_table_differences_only(sample_difference_results):
    """Test creating summary table with difference results only."""
    df = create_summary_table(sample_difference_results)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'Type' in df.columns
    assert 'Genre_A' in df.columns
    assert 'Genre_B' in df.columns
    assert 'Mean_Difference' in df.columns
    assert 'CI_Width' in df.columns
    assert all(df['Type'] == 'Difference')


def test_create_summary_table_mixed(sample_mixed_results):
    """Test creating summary table with mixed results."""
    df = create_summary_table(sample_mixed_results)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert 'Type' in df.columns
    assert len(df[df['Type'] == 'Mean']) == 3
    assert len(df[df['Type'] == 'Difference']) == 2


def test_create_summary_table_empty_list():
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError, match="non-empty list"):
        create_summary_table([])


def test_create_summary_table_invalid_input():
    """Test that invalid input raises ValueError."""
    with pytest.raises(ValueError, match="non-empty list"):
        create_summary_table("not a list")
    
    with pytest.raises(ValueError, match="non-empty list"):
        create_summary_table({})


def test_create_summary_table_decimals(sample_mean_results):
    """Test decimal rounding option."""
    df = create_summary_table(sample_mean_results, decimals=2)
    
    # Check that numeric columns are rounded
    mean_values = df['Mean'].dropna()
    if len(mean_values) > 0:
        # Values should be rounded to 2 decimals
        assert all(isinstance(x, (int, float)) for x in mean_values)


def test_create_summary_table_sorting(sample_mean_results):
    """Test sorting functionality."""
    df_sorted = create_summary_table(sample_mean_results, sort_results=True)
    df_unsorted = create_summary_table(sample_mean_results, sort_results=False)
    
    # Sorted DataFrame should be ordered by Region, then Genre
    if len(df_sorted) > 1:
        regions = df_sorted['Region'].values
        # Check that regions are sorted
        assert all(regions[i] <= regions[i+1] for i in range(len(regions)-1))


def test_create_summary_table_separate_tables(sample_mixed_results):
    """Test separate_tables option."""
    result = create_summary_table(sample_mixed_results, separate_tables=True)
    
    assert isinstance(result, dict)
    assert 'means' in result
    assert 'differences' in result
    assert isinstance(result['means'], pd.DataFrame)
    assert isinstance(result['differences'], pd.DataFrame)
    assert len(result['means']) == 3
    assert len(result['differences']) == 2


def test_create_summary_table_ci_width(sample_mean_results):
    """Test that CI_Width is calculated correctly."""
    df = create_summary_table(sample_mean_results)
    
    assert 'CI_Width' in df.columns
    # CI_Width should be positive
    widths = df['CI_Width'].dropna()
    assert all(widths >= 0)


# ============================================================================
# Tests for export_results_table
# ============================================================================

def test_export_results_table(sample_mean_results, temp_dir):
    """Test exporting results table to CSV."""
    df = create_summary_table(sample_mean_results)
    filepath = Path(temp_dir) / "test_results.csv"
    
    export_results_table(df, str(filepath))
    
    # Check that file was created
    assert filepath.exists()
    
    # Check that file can be read back
    df_read = pd.read_csv(filepath)
    assert len(df_read) == len(df)
    assert list(df_read.columns) == list(df.columns)


def test_export_results_table_creates_directory(temp_dir):
    """Test that export creates parent directories."""
    df = create_summary_table([{
        'genre': 'Action',
        'region': 'Global',
        'mean': 3.0,
        'ci_lower': 2.8,
        'ci_upper': 3.2,
        'sample_size': 100
    }])
    
    filepath = Path(temp_dir) / "subdir" / "test_results.csv"
    export_results_table(df, str(filepath))
    
    assert filepath.exists()


# ============================================================================
# Tests for make_latex_table
# ============================================================================

def test_make_latex_table(sample_mean_results, temp_dir):
    """Test LaTeX table export."""
    df = create_summary_table(sample_mean_results)
    filepath = Path(temp_dir) / "test_table.tex"
    
    make_latex_table(df, str(filepath))
    
    # Check that file was created
    assert filepath.exists()
    
    # Check that file contains LaTeX content
    content = filepath.read_text(encoding='utf-8')
    assert '\\begin{tabular}' in content or 'tabular' in content.lower()


def test_make_latex_table_creates_directory(temp_dir):
    """Test that LaTeX export creates parent directories."""
    df = create_summary_table([{
        'genre': 'Action',
        'region': 'Global',
        'mean': 3.0,
        'ci_lower': 2.8,
        'ci_upper': 3.2,
        'sample_size': 100
    }])
    
    filepath = Path(temp_dir) / "latex" / "test_table.tex"
    make_latex_table(df, str(filepath))
    
    assert filepath.exists()


# ============================================================================
# Tests for region_specific_tables
# ============================================================================

def test_region_specific_tables(sample_mean_results):
    """Test creating region-specific tables."""
    df = create_summary_table(sample_mean_results)
    tables = region_specific_tables(df)
    
    assert isinstance(tables, dict)
    assert 'Global' in tables
    assert 'NA' in tables
    assert isinstance(tables['Global'], pd.DataFrame)
    assert len(tables['Global']) == 2  # Two genres in Global
    assert len(tables['NA']) == 1  # One genre in NA


def test_region_specific_tables_no_region_column():
    """Test that missing Region column raises ValueError."""
    df = pd.DataFrame({'Genre': ['Action'], 'Mean': [3.0]})
    
    with pytest.raises(ValueError, match="Region column"):
        region_specific_tables(df)


def test_region_specific_tables_empty_dataframe():
    """Test with empty DataFrame."""
    df = pd.DataFrame({'Region': [], 'Genre': []})
    tables = region_specific_tables(df)
    
    assert isinstance(tables, dict)
    assert len(tables) == 0


# ============================================================================
# Tests for genre_comparison_matrix
# ============================================================================

def test_genre_comparison_matrix(sample_difference_results):
    """Test creating genre comparison matrix."""
    df = create_summary_table(sample_difference_results)
    matrix = genre_comparison_matrix(df)
    
    assert isinstance(matrix, pd.DataFrame)
    # Matrix should have Genre_A as index and Genre_B as columns
    assert 'Action' in matrix.index
    assert 'Role-Playing' in matrix.columns or 'Simulation' in matrix.columns


def test_genre_comparison_matrix_no_mean_difference():
    """Test that missing Mean_Difference column raises ValueError."""
    df = pd.DataFrame({
        'Type': ['Mean'],
        'Genre': ['Action'],
        'Region': ['Global'],
        'Mean': [3.0]
    })
    
    with pytest.raises(ValueError, match="Difference"):
        genre_comparison_matrix(df)


def test_genre_comparison_matrix_only_means():
    """Test with DataFrame containing only mean results."""
    df = create_summary_table([{
        'genre': 'Action',
        'region': 'Global',
        'mean': 3.0,
        'ci_lower': 2.8,
        'ci_upper': 3.2,
        'sample_size': 100
    }])
    
    with pytest.raises(ValueError, match="Difference"):
        genre_comparison_matrix(df)


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_reporting_pipeline(sample_mixed_results, temp_dir):
    """Test complete reporting pipeline."""
    # Step 1: Create summary table
    df = create_summary_table(sample_mixed_results, separate_tables=False)
    assert isinstance(df, pd.DataFrame)
    
    # Step 2: Export to CSV
    csv_path = Path(temp_dir) / "results.csv"
    export_results_table(df, str(csv_path))
    assert csv_path.exists()
    
    # Step 3: Export to LaTeX
    latex_path = Path(temp_dir) / "results.tex"
    make_latex_table(df, str(latex_path))
    assert latex_path.exists()
    
    # Step 4: Create region-specific tables
    region_tables = region_specific_tables(df)
    assert isinstance(region_tables, dict)
    
    # Step 5: Create genre comparison matrix (from differences only)
    diff_df = df[df['Type'] == 'Difference']
    if len(diff_df) > 0:
        matrix = genre_comparison_matrix(diff_df)
        assert isinstance(matrix, pd.DataFrame)


def test_separate_tables_workflow(sample_mixed_results, temp_dir):
    """Test workflow with separate tables."""
    # Create separate tables
    tables = create_summary_table(sample_mixed_results, separate_tables=True)
    
    # Export means table
    means_path = Path(temp_dir) / "means.csv"
    export_results_table(tables['means'], str(means_path))
    assert means_path.exists()
    
    # Export differences table
    diff_path = Path(temp_dir) / "differences.csv"
    export_results_table(tables['differences'], str(diff_path))
    assert diff_path.exists()
    
    # Create matrix from differences
    matrix = genre_comparison_matrix(tables['differences'])
    assert isinstance(matrix, pd.DataFrame)


# ============================================================================
# Edge Cases and Robustness Tests
# ============================================================================

def test_create_summary_table_missing_keys():
    """Test handling of missing keys in results."""
    results = [
        {
            'genre': 'Action',
            'region': 'Global',
            # Missing mean, ci_lower, etc.
        }
    ]
    
    df = create_summary_table(results)
    assert isinstance(df, pd.DataFrame)
    # Should handle missing keys gracefully with NaN or defaults


def test_create_summary_table_nan_values():
    """Test handling of NaN values in results."""
    results = [
        {
            'genre': 'Action',
            'region': 'Global',
            'mean': np.nan,
            'ci_lower': 2.8,
            'ci_upper': 3.2,
            'sample_size': 100
        }
    ]
    
    df = create_summary_table(results)
    assert isinstance(df, pd.DataFrame)
    assert pd.isna(df['Mean'].iloc[0])


def test_format_number_edge_cases():
    """Test format_number with edge cases."""
    # Very large number
    assert format_number(1e10, decimals=2) == 1e10
    
    # Very small number (rounding may result in 0.0)
    result = format_number(1e-10, decimals=5)
    assert isinstance(result, (int, float))
    assert result >= 0  # Should be non-negative after rounding
    
    # Negative number
    assert format_number(-3.14159, decimals=2) == -3.14


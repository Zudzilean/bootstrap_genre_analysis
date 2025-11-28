"""
Unit tests for visualization module.

Tests cover:
- Bootstrap distribution plotting
- Confidence interval plotting
- Regional comparison plotting
- Input validation and error handling
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import tempfile
import shutil
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt

# Add project root to path
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


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_bootstrap_stats():
    """Create sample bootstrap statistics."""
    np.random.seed(42)
    return np.random.normal(3.0, 0.5, size=10000)


@pytest.fixture
def sample_bootstrap_results():
    """Create sample bootstrap results dictionary."""
    return {
        ('Action', 'Global'): {
            'genre': 'Action',
            'region': 'Global',
            'mean': 3.0,
            'bootstrap_means': np.random.normal(3.0, 0.1, 1000),
            'sample_size': 100
        },
        ('Action', 'NA'): {
            'genre': 'Action',
            'region': 'NA',
            'mean': 2.8,
            'bootstrap_means': np.random.normal(2.8, 0.1, 1000),
            'sample_size': 95
        },
        ('Role-Playing', 'Global'): {
            'genre': 'Role-Playing',
            'region': 'Global',
            'mean': 2.9,
            'bootstrap_means': np.random.normal(2.9, 0.1, 1000),
            'sample_size': 80
        },
        ('Simulation', 'Global'): {
            'genre': 'Simulation',
            'region': 'Global',
            'mean': 2.5,
            'bootstrap_means': np.random.normal(2.5, 0.1, 1000),
            'sample_size': 60
        }
    }


@pytest.fixture
def sample_ci_results():
    """Create sample confidence interval results DataFrame."""
    return pd.DataFrame({
        'genre': ['Action', 'Role-Playing', 'Simulation'],
        'region': ['Global', 'Global', 'Global'],
        'mean': [3.0, 2.9, 2.5],
        'ci_lower': [2.8, 2.7, 2.3],
        'ci_upper': [3.2, 3.1, 2.7]
    })


@pytest.fixture
def sample_difference_results():
    """Create sample difference results dictionary."""
    return {
        ('Action', 'Role-Playing', 'Global'): {
            'genre_A': 'Action',
            'genre_B': 'Role-Playing',
            'region': 'Global',
            'mean_difference': 0.1,
            'bootstrap_differences': np.random.normal(0.1, 0.15, 10000),
            'sample_size_A': 100,
            'sample_size_B': 80
        },
        ('Action', 'Simulation', 'Global'): {
            'genre_A': 'Action',
            'genre_B': 'Simulation',
            'region': 'Global',
            'mean_difference': 0.5,
            'bootstrap_differences': np.random.normal(0.5, 0.2, 10000),
            'sample_size_A': 100,
            'sample_size_B': 60
        }
    }


@pytest.fixture
def temp_dir():
    """Create temporary directory for test outputs."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


# ============================================================================
# Tests for plot_bootstrap_distribution
# ============================================================================

def test_plot_bootstrap_distribution_basic(sample_bootstrap_stats, temp_dir):
    """Test basic bootstrap distribution plotting."""
    save_path = Path(temp_dir) / "test_bootstrap.png"
    
    plot_bootstrap_distribution(
        sample_bootstrap_stats,
        true_statistic=3.0,
        ci_bounds=(2.5, 3.5),
        title="Test Bootstrap Distribution",
        save_path=str(save_path)
    )
    
    # Check that file was created
    assert save_path.exists()
    plt.close('all')


def test_plot_bootstrap_distribution_without_ci(sample_bootstrap_stats):
    """Test plotting without confidence interval."""
    plot_bootstrap_distribution(
        sample_bootstrap_stats,
        true_statistic=3.0,
        title="Test Without CI"
    )
    plt.close('all')


def test_plot_bootstrap_distribution_without_statistic(sample_bootstrap_stats):
    """Test plotting without observed statistic."""
    plot_bootstrap_distribution(
        sample_bootstrap_stats,
        ci_bounds=(2.5, 3.5),
        title="Test Without Statistic"
    )
    plt.close('all')


def test_plot_bootstrap_distribution_empty_data():
    """Test that empty data raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_bootstrap_distribution(np.array([]))
    plt.close('all')


def test_plot_bootstrap_distribution_invalid_ci(sample_bootstrap_stats):
    """Test that invalid CI bounds raise ValueError."""
    with pytest.raises(ValueError, match="must be a tuple"):
        plot_bootstrap_distribution(sample_bootstrap_stats, ci_bounds=(2.5,))
    plt.close('all')


# ============================================================================
# Tests for plot_genre_means_by_region
# ============================================================================

def test_plot_genre_means_by_region_basic(sample_bootstrap_results, temp_dir):
    """Test basic genre means by region plotting."""
    save_path = Path(temp_dir) / "test_genre_means.png"
    
    plot_genre_means_by_region(
        sample_bootstrap_results,
        save_path=str(save_path)
    )
    
    # Check that file was created
    assert save_path.exists()
    plt.close('all')


def test_plot_genre_means_by_region_empty_dict():
    """Test that empty results dictionary raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_genre_means_by_region({})
    plt.close('all')


def test_plot_genre_means_by_region_with_string_keys():
    """Test plotting with string keys instead of tuples."""
    results = {
        'Action_Global': {
            'genre': 'Action',
            'region': 'Global',
            'mean': 3.0,
            'sample_size': 100
        }
    }
    plot_genre_means_by_region(results)
    plt.close('all')


# ============================================================================
# Tests for plot_confidence_intervals
# ============================================================================

def test_plot_confidence_intervals_basic(sample_ci_results, temp_dir):
    """Test basic confidence interval plotting."""
    save_path = Path(temp_dir) / "test_ci.png"
    
    plot_confidence_intervals(
        sample_ci_results,
        save_path=str(save_path),
        title="Test Confidence Intervals"
    )
    
    # Check that file was created
    assert save_path.exists()
    plt.close('all')


def test_plot_confidence_intervals_empty_dataframe():
    """Test that empty DataFrame raises ValueError."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_confidence_intervals(empty_df)
    plt.close('all')


def test_plot_confidence_intervals_missing_columns():
    """Test that missing required columns raise ValueError."""
    incomplete_df = pd.DataFrame({
        'genre': ['Action'],
        'mean': [3.0]
        # Missing ci_lower and ci_upper
    })
    with pytest.raises(ValueError, match="Missing required columns"):
        plot_confidence_intervals(incomplete_df)
    plt.close('all')


def test_plot_confidence_intervals_with_region(sample_ci_results):
    """Test plotting with region column."""
    plot_confidence_intervals(sample_ci_results)
    plt.close('all')


# ============================================================================
# Tests for plot_regional_comparison
# ============================================================================

def test_plot_regional_comparison_basic(sample_bootstrap_results, temp_dir):
    """Test basic regional comparison plotting."""
    save_path = Path(temp_dir) / "test_regional.png"
    
    plot_regional_comparison(
        sample_bootstrap_results,
        save_path=str(save_path),
        title="Test Regional Comparison"
    )
    
    # Check that file was created
    assert save_path.exists()
    plt.close('all')


def test_plot_regional_comparison_empty_dict():
    """Test that empty results dictionary raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_regional_comparison({})
    plt.close('all')


def test_plot_regional_comparison_single_region():
    """Test plotting with single region."""
    results = {
        ('Action', 'Global'): {
            'genre': 'Action',
            'region': 'Global',
            'mean': 3.0
        }
    }
    plot_regional_comparison(results)
    plt.close('all')


# ============================================================================
# Tests for plot_difference_distributions
# ============================================================================

def test_plot_difference_distributions_basic(sample_difference_results, temp_dir):
    """Test basic difference distributions plotting."""
    save_path = Path(temp_dir) / "test_differences.png"
    
    plot_difference_distributions(
        sample_difference_results,
        save_path=str(save_path),
        title="Test Difference Distributions"
    )
    
    # Check that file was created
    assert save_path.exists()
    plt.close('all')


def test_plot_difference_distributions_empty_dict():
    """Test that empty results dictionary raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_difference_distributions({})
    plt.close('all')


def test_plot_difference_distributions_no_bootstrap_diffs():
    """Test that missing bootstrap_differences raises ValueError."""
    results = {
        'test': {
            'genre_A': 'Action',
            'genre_B': 'Role-Playing',
            'mean_difference': 0.1
            # Missing bootstrap_differences
        }
    }
    with pytest.raises(ValueError, match="No 'bootstrap_differences'"):
        plot_difference_distributions(results)
    plt.close('all')


def test_plot_difference_distributions_single_comparison():
    """Test plotting with single genre comparison."""
    results = {
        'test': {
            'genre_A': 'Action',
            'genre_B': 'Role-Playing',
            'region': 'Global',
            'bootstrap_differences': np.random.normal(0.1, 0.15, 1000)
        }
    }
    plot_difference_distributions(results)
    plt.close('all')


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_visualization_pipeline(sample_bootstrap_stats, sample_ci_results, temp_dir):
    """Test complete visualization pipeline."""
    # Step 1: Plot bootstrap distribution
    bootstrap_path = Path(temp_dir) / "bootstrap_dist.png"
    plot_bootstrap_distribution(
        sample_bootstrap_stats,
        true_statistic=3.0,
        ci_bounds=(2.5, 3.5),
        save_path=str(bootstrap_path)
    )
    assert bootstrap_path.exists()
    
    # Step 2: Plot confidence intervals
    ci_path = Path(temp_dir) / "ci_plot.png"
    plot_confidence_intervals(
        sample_ci_results,
        save_path=str(ci_path)
    )
    assert ci_path.exists()
    
    plt.close('all')


def test_visualization_with_real_data_format(sample_bootstrap_results, sample_difference_results, temp_dir):
    """Test visualization functions with realistic data structures."""
    # Test genre means plot
    means_path = Path(temp_dir) / "means.png"
    plot_genre_means_by_region(sample_bootstrap_results, save_path=str(means_path))
    assert means_path.exists()
    
    # Test difference distributions
    diff_path = Path(temp_dir) / "differences.png"
    plot_difference_distributions(sample_difference_results, save_path=str(diff_path))
    assert diff_path.exists()
    
    plt.close('all')


# ============================================================================
# Edge Cases and Robustness Tests
# ============================================================================

def test_plot_bootstrap_distribution_small_sample():
    """Test plotting with very small bootstrap sample."""
    small_stats = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    plot_bootstrap_distribution(small_stats, true_statistic=3.0)
    plt.close('all')


def test_plot_confidence_intervals_single_row():
    """Test plotting with single row DataFrame."""
    single_row = pd.DataFrame({
        'genre': ['Action'],
        'mean': [3.0],
        'ci_lower': [2.8],
        'ci_upper': [3.2]
    })
    plot_confidence_intervals(single_row)
    plt.close('all')


def test_plot_regional_comparison_missing_mean():
    """Test plotting with missing mean values (should handle NaN)."""
    results = {
        ('Action', 'Global'): {
            'genre': 'Action',
            'region': 'Global',
            'mean': np.nan  # Missing mean
        }
    }
    # Should not raise error, but may produce empty plot
    plot_regional_comparison(results)
    plt.close('all')


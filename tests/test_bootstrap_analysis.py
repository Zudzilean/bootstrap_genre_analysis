"""
Unit tests for bootstrap analysis module.

Tests cover:
- Bootstrap mean estimation
- Bootstrap difference estimation
- Confidence interval calculation
- Statistical correctness and edge cases
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.bootstrap_analysis.bootstrap_means import (
    bootstrap_mean,
    bootstrap_genre_mean_by_region
)
from src.bootstrap_analysis.bootstrap_differences import (
    bootstrap_difference,
    bootstrap_genre_difference
)
from src.bootstrap_analysis.confidence_intervals import (
    percentile_ci,
    is_significant
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    return np.random.normal(3.0, 0.5, size=100)


@pytest.fixture
def sample_dataframe():
    """Create sample DataFrame for testing."""
    data = {
        'Genre': ['Action'] * 50 + ['Role-Playing'] * 30 + ['Simulation'] * 20,
        'log_sales': np.concatenate([
            np.random.normal(3.0, 0.5, 50),
            np.random.normal(2.8, 0.4, 30),
            np.random.normal(2.5, 0.3, 20)
        ]),
        'Year': [2010] * 100,
        'Platform': ['PS4'] * 100
    }
    return pd.DataFrame(data)


# ============================================================================
# Tests for bootstrap_mean
# ============================================================================

def test_bootstrap_mean_basic(sample_data):
    """Test basic bootstrap mean functionality."""
    result = bootstrap_mean(sample_data, n_iterations=1000, random_seed=42)
    
    assert len(result) == 1000
    assert isinstance(result, np.ndarray)
    assert np.all(np.isfinite(result))
    # Bootstrap mean should be close to sample mean
    assert np.abs(result.mean() - sample_data.mean()) < 0.1


def test_bootstrap_mean_reproducibility(sample_data):
    """Test that bootstrap mean is reproducible with same seed."""
    result1 = bootstrap_mean(sample_data, n_iterations=100, random_seed=42)
    result2 = bootstrap_mean(sample_data, n_iterations=100, random_seed=42)
    
    np.testing.assert_array_equal(result1, result2)


def test_bootstrap_mean_different_seeds(sample_data):
    """Test that different seeds produce different results."""
    result1 = bootstrap_mean(sample_data, n_iterations=100, random_seed=42)
    result2 = bootstrap_mean(sample_data, n_iterations=100, random_seed=123)
    
    # Results should be different (very unlikely to be identical)
    assert not np.array_equal(result1, result2)


def test_bootstrap_mean_empty_data():
    """Test that empty data raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        bootstrap_mean(np.array([]), n_iterations=100)


def test_bootstrap_mean_invalid_iterations(sample_data):
    """Test that invalid n_iterations raises ValueError."""
    with pytest.raises(ValueError, match="must be positive"):
        bootstrap_mean(sample_data, n_iterations=0)
    
    with pytest.raises(ValueError, match="must be positive"):
        bootstrap_mean(sample_data, n_iterations=-1)


def test_bootstrap_mean_single_value():
    """Test bootstrap with single data point."""
    data = np.array([3.5])
    result = bootstrap_mean(data, n_iterations=100, random_seed=42)
    
    assert len(result) == 100
    # All bootstrap means should equal the single value
    assert np.allclose(result, 3.5)


def test_bootstrap_mean_small_sample():
    """Test bootstrap with very small sample."""
    data = np.array([1.0, 2.0, 3.0])
    result = bootstrap_mean(data, n_iterations=100, random_seed=42)
    
    assert len(result) == 100
    assert np.all(np.isfinite(result))
    # Mean should be around 2.0
    assert 1.5 < result.mean() < 2.5


# ============================================================================
# Tests for bootstrap_genre_mean_by_region
# ============================================================================

def test_bootstrap_genre_mean_by_region_basic(sample_dataframe):
    """Test basic bootstrap genre mean by region functionality."""
    result = bootstrap_genre_mean_by_region(
        sample_dataframe, 
        genre='Action', 
        region='Global',
        n_iterations=1000,
        random_seed=42
    )
    
    assert isinstance(result, dict)
    assert 'genre' in result
    assert 'region' in result
    assert 'mean' in result
    assert 'bootstrap_means' in result
    assert 'sample_size' in result
    
    assert result['genre'] == 'Action'
    assert result['region'] == 'Global'
    assert result['sample_size'] == 50
    assert len(result['bootstrap_means']) == 1000
    assert np.abs(result['mean'] - sample_dataframe[sample_dataframe['Genre'] == 'Action']['log_sales'].mean()) < 0.01


def test_bootstrap_genre_mean_by_region_missing_columns():
    """Test that missing columns raise ValueError."""
    df = pd.DataFrame({'Genre': ['Action'], 'sales': [3.0]})
    
    with pytest.raises(ValueError, match="must contain"):
        bootstrap_genre_mean_by_region(df, 'Action', 'Global')


def test_bootstrap_genre_mean_by_region_nonexistent_genre(sample_dataframe):
    """Test that nonexistent genre raises ValueError."""
    with pytest.raises(ValueError, match="No data found"):
        bootstrap_genre_mean_by_region(sample_dataframe, 'Nonexistent', 'Global')


# ============================================================================
# Tests for bootstrap_difference
# ============================================================================

def test_bootstrap_difference_basic():
    """Test basic bootstrap difference functionality."""
    data_A = np.random.normal(3.0, 0.5, size=50)
    data_B = np.random.normal(2.5, 0.4, size=40)
    
    result = bootstrap_difference(data_A, data_B, n_iterations=1000, random_seed=42)
    
    assert len(result) == 1000
    assert isinstance(result, np.ndarray)
    assert np.all(np.isfinite(result))
    # Mean difference should be positive (A > B)
    assert result.mean() > 0


def test_bootstrap_difference_reproducibility():
    """Test that bootstrap difference is reproducible with same seed."""
    data_A = np.random.normal(3.0, 0.5, size=50)
    data_B = np.random.normal(2.5, 0.4, size=40)
    
    result1 = bootstrap_difference(data_A, data_B, n_iterations=100, random_seed=42)
    result2 = bootstrap_difference(data_A, data_B, n_iterations=100, random_seed=42)
    
    np.testing.assert_array_equal(result1, result2)


def test_bootstrap_difference_empty_data():
    """Test that empty data raises ValueError."""
    data = np.array([1.0, 2.0, 3.0])
    
    with pytest.raises(ValueError, match="must be non-empty"):
        bootstrap_difference(np.array([]), data, n_iterations=100)
    
    with pytest.raises(ValueError, match="must be non-empty"):
        bootstrap_difference(data, np.array([]), n_iterations=100)


def test_bootstrap_difference_invalid_iterations():
    """Test that invalid n_iterations raises ValueError."""
    data_A = np.array([1.0, 2.0, 3.0])
    data_B = np.array([2.0, 3.0, 4.0])
    
    with pytest.raises(ValueError, match="must be positive"):
        bootstrap_difference(data_A, data_B, n_iterations=0)


def test_bootstrap_difference_independence():
    """Test that bootstrap resampling is independent for each group."""
    # Use same data for both groups - difference should be around zero
    data = np.random.normal(3.0, 0.5, size=50)
    
    result = bootstrap_difference(data, data, n_iterations=1000, random_seed=42)
    
    # Mean difference should be close to zero
    assert np.abs(result.mean()) < 0.1
    # But variance should be positive (due to bootstrap resampling)
    assert result.std() > 0


# ============================================================================
# Tests for bootstrap_genre_difference
# ============================================================================

def test_bootstrap_genre_difference_basic(sample_dataframe):
    """Test basic bootstrap genre difference functionality."""
    result = bootstrap_genre_difference(
        sample_dataframe,
        genre_A='Action',
        genre_B='Role-Playing',
        region='Global',
        n_iterations=1000,
        random_seed=42
    )
    
    assert isinstance(result, dict)
    assert 'genre_A' in result
    assert 'genre_B' in result
    assert 'region' in result
    assert 'mean_difference' in result
    assert 'bootstrap_differences' in result
    assert 'sample_size_A' in result
    assert 'sample_size_B' in result
    assert 'mean_A' in result
    assert 'mean_B' in result
    
    assert result['genre_A'] == 'Action'
    assert result['genre_B'] == 'Role-Playing'
    assert result['region'] == 'Global'
    assert result['sample_size_A'] == 50
    assert result['sample_size_B'] == 30
    assert len(result['bootstrap_differences']) == 1000


def test_bootstrap_genre_difference_missing_columns():
    """Test that missing columns raise ValueError."""
    df = pd.DataFrame({'Genre': ['Action'], 'sales': [3.0]})
    
    with pytest.raises(ValueError, match="must contain"):
        bootstrap_genre_difference(df, 'Action', 'Role-Playing', 'Global')


def test_bootstrap_genre_difference_nonexistent_genre(sample_dataframe):
    """Test that nonexistent genre raises ValueError."""
    with pytest.raises(ValueError, match="No data found"):
        bootstrap_genre_difference(sample_dataframe, 'Nonexistent', 'Action', 'Global')
    
    with pytest.raises(ValueError, match="No data found"):
        bootstrap_genre_difference(sample_dataframe, 'Action', 'Nonexistent', 'Global')


# ============================================================================
# Tests for percentile_ci
# ============================================================================

def test_percentile_ci_basic():
    """Test basic percentile CI calculation."""
    bootstrap_stats = np.random.normal(3.0, 0.1, size=10000)
    ci_lower, ci_upper = percentile_ci(bootstrap_stats, confidence_level=0.95)
    
    assert ci_lower < ci_upper
    assert ci_lower < 3.0 < ci_upper
    # For 95% CI, should cover approximately 95% of data
    coverage = np.sum((bootstrap_stats >= ci_lower) & (bootstrap_stats <= ci_upper)) / len(bootstrap_stats)
    assert 0.94 < coverage < 0.96  # Allow small margin


def test_percentile_ci_different_levels():
    """Test percentile CI with different confidence levels."""
    bootstrap_stats = np.random.normal(3.0, 0.1, size=10000)
    
    ci_90 = percentile_ci(bootstrap_stats, confidence_level=0.90)
    ci_95 = percentile_ci(bootstrap_stats, confidence_level=0.95)
    ci_99 = percentile_ci(bootstrap_stats, confidence_level=0.99)
    
    # Higher confidence should give wider intervals
    assert (ci_99[1] - ci_99[0]) > (ci_95[1] - ci_95[0])
    assert (ci_95[1] - ci_95[0]) > (ci_90[1] - ci_90[0])


def test_percentile_ci_empty_data():
    """Test that empty data raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        percentile_ci(np.array([]))


def test_percentile_ci_invalid_confidence_level():
    """Test that invalid confidence level raises ValueError."""
    bootstrap_stats = np.array([1.0, 2.0, 3.0])
    
    with pytest.raises(ValueError, match="must be between"):
        percentile_ci(bootstrap_stats, confidence_level=0.0)
    
    with pytest.raises(ValueError, match="must be between"):
        percentile_ci(bootstrap_stats, confidence_level=1.0)
    
    with pytest.raises(ValueError, match="must be between"):
        percentile_ci(bootstrap_stats, confidence_level=1.5)


# ============================================================================
# Tests for is_significant
# ============================================================================

def test_is_significant_excludes_zero():
    """Test that CI excluding zero is significant."""
    assert is_significant(0.1, 0.5) == True
    assert is_significant(-0.5, -0.1) == True


def test_is_significant_includes_zero():
    """Test that CI including zero is not significant."""
    assert is_significant(-0.1, 0.1) == False
    assert is_significant(-0.5, 0.5) == False


def test_is_significant_boundary_cases():
    """Test boundary cases for significance testing."""
    # CI exactly at zero (lower bound = 0) - 0 is included, so not significant
    # Standard statistical interpretation: if CI contains null_value, not significant
    assert is_significant(0.0, 0.5) == False
    
    # CI exactly at zero (upper bound = 0) - 0 is included, so not significant
    assert is_significant(-0.5, 0.0) == False
    
    # CI includes zero (strictly includes)
    assert is_significant(-0.1, 0.1) == False
    
    # CI excludes zero (strictly positive)
    assert is_significant(0.001, 0.5) == True
    
    # CI excludes zero (strictly negative)
    assert is_significant(-0.5, -0.001) == True


def test_is_significant_custom_null_value():
    """Test significance testing with custom null value."""
    # CI excludes 1.0
    assert is_significant(1.1, 1.5, null_value=1.0) == True
    
    # CI includes 1.0
    assert is_significant(0.9, 1.1, null_value=1.0) == False


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_bootstrap_pipeline(sample_dataframe):
    """Test complete bootstrap pipeline from data to CI."""
    # Step 1: Bootstrap mean for a genre
    result = bootstrap_genre_mean_by_region(
        sample_dataframe,
        genre='Action',
        region='Global',
        n_iterations=1000,
        random_seed=42
    )
    
    # Step 2: Calculate confidence interval
    ci_lower, ci_upper = percentile_ci(result['bootstrap_means'], confidence_level=0.95)
    
    # Step 3: Verify results are reasonable
    assert ci_lower < result['mean'] < ci_upper
    assert ci_lower < ci_upper


def test_full_difference_pipeline(sample_dataframe):
    """Test complete bootstrap difference pipeline."""
    # Step 1: Bootstrap difference between genres
    result = bootstrap_genre_difference(
        sample_dataframe,
        genre_A='Action',
        genre_B='Role-Playing',
        region='Global',
        n_iterations=1000,
        random_seed=42
    )
    
    # Step 2: Calculate confidence interval
    ci_lower, ci_upper = percentile_ci(result['bootstrap_differences'], confidence_level=0.95)
    
    # Step 3: Test significance
    significant = is_significant(ci_lower, ci_upper)
    
    # Step 4: Verify results are reasonable
    assert ci_lower < result['mean_difference'] < ci_upper
    assert isinstance(significant, bool)


def test_bootstrap_statistical_properties():
    """Test that bootstrap produces statistically reasonable results."""
    # Create data with known mean
    true_mean = 3.0
    data = np.random.normal(true_mean, 0.5, size=100)
    
    # Run bootstrap
    bootstrap_means = bootstrap_mean(data, n_iterations=10000, random_seed=42)
    
    # Bootstrap mean should be close to sample mean
    assert np.abs(bootstrap_means.mean() - data.mean()) < 0.05
    
    # Bootstrap standard error should be reasonable
    bootstrap_se = bootstrap_means.std()
    sample_se = data.std() / np.sqrt(len(data))
    # Bootstrap SE should be similar to theoretical SE (within factor of 2)
    assert 0.5 < bootstrap_se / sample_se < 2.0



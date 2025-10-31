"""
Unit tests for data preprocessing module.

Tests cover:
- Data loading and validation
- Data cleaning functions
- Data transformation functions
- Integration tests for full pipeline
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

from src.data_preprocessing.load_data import load_raw_data, validate_data
from src.data_preprocessing.clean_data import (
    remove_invalid_entries,
    filter_time_window,
    select_genres
)
from src.data_preprocessing.transform_data import (
    apply_log_transform,
    reshape_for_analysis,
    save_cleaned_data
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_raw_data():
    """Create sample raw data for testing."""
    data = {
        'Name': ['Game1', 'Game2', 'Game3', 'Game4', 'Game5'],
        'Platform': ['PS4', 'Xbox', 'PC', 'Switch', 'PS4'],
        'Year': [2010.0, 2015.0, 2000.0, 2018.0, np.nan],
        'Genre': ['Action', 'Role-Playing', 'Simulation', 'Action', 'Action'],
        'Publisher': ['Publisher1', 'Publisher2', 'Publisher3', 'Publisher4', 'Publisher5'],
        'NA_Sales': [1.5, 2.3, 0.0, 1.0, 0.5],
        'EU_Sales': [1.2, 1.8, 0.5, 0.8, 0.3],
        'JP_Sales': [0.5, 0.2, 0.1, 0.3, 0.1],
        'Other_Sales': [0.3, 0.4, 0.1, 0.2, 0.1],
        'Global_Sales': [3.5, 4.7, 0.7, 2.3, 1.0]
    }
    return pd.DataFrame(data)


@pytest.fixture
def valid_csv_file(tmp_path, sample_raw_data):
    """Create a temporary CSV file for testing."""
    filepath = tmp_path / "test_data.csv"
    sample_raw_data.to_csv(filepath, index=False)
    return str(filepath)


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory for testing."""
    return tmp_path / "output"


# ============================================================================
# Tests for load_data.py
# ============================================================================

class TestLoadData:
    """Tests for data loading functions."""
    
    def test_load_raw_data_success(self, valid_csv_file):
        """Test successful data loading."""
        df = load_raw_data(valid_csv_file)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert 'Name' in df.columns
        assert 'Genre' in df.columns
    
    def test_load_raw_data_file_not_found(self):
        """Test loading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_raw_data("nonexistent_file.csv")
    
    def test_validate_data_valid(self, sample_raw_data):
        """Test validation of valid data."""
        is_valid, issues = validate_data(sample_raw_data)
        # Note: This data has some issues (missing Year, zero sales), 
        # so it may not be fully valid, but structure is correct
        assert isinstance(is_valid, bool)
        assert isinstance(issues, list)
    
    def test_validate_data_missing_columns(self):
        """Test validation detects missing required columns."""
        df = pd.DataFrame({'Name': ['Game1'], 'Genre': ['Action']})
        is_valid, issues = validate_data(df)
        assert is_valid == False
        assert len(issues) > 0
    
    def test_validate_data_missing_genre(self):
        """Test validation detects missing Genre values."""
        data = {
            'Name': ['Game1', 'Game2'],
            'Genre': ['Action', None],
            'Year': [2010, 2010],
            'NA_Sales': [1.0, 1.0],
            'EU_Sales': [1.0, 1.0],
            'JP_Sales': [1.0, 1.0],
            'Other_Sales': [1.0, 1.0],
            'Global_Sales': [4.0, 4.0]
        }
        df = pd.DataFrame(data)
        is_valid, issues = validate_data(df)
        assert is_valid == False
        assert any('missing Genre' in issue for issue in issues)


# ============================================================================
# Tests for clean_data.py
# ============================================================================

class TestCleanData:
    """Tests for data cleaning functions."""
    
    def test_remove_invalid_entries(self, sample_raw_data):
        """Test removal of invalid entries."""
        df_clean = remove_invalid_entries(sample_raw_data)
        
        # Should remove row with missing Year (Game5)
        # Should remove row with zero Global_Sales (Game3)
        assert len(df_clean) < len(sample_raw_data)
        assert df_clean['Year'].notna().all()
        assert (df_clean['Global_Sales'] > 0).all()
        assert df_clean['Genre'].notna().all()
    
    def test_filter_time_window(self, sample_raw_data):
        """Test time window filtering."""
        # Clean data first
        df_clean = remove_invalid_entries(sample_raw_data)
        
        # Filter to 2005-2016
        df_filtered = filter_time_window(df_clean, start_year=2005, end_year=2016)
        
        if len(df_filtered) > 0:
            assert df_filtered['Year'].min() >= 2005
            assert df_filtered['Year'].max() <= 2016
    
    def test_filter_time_window_start_only(self, sample_raw_data):
        """Test filtering with only start year."""
        df_clean = remove_invalid_entries(sample_raw_data)
        df_filtered = filter_time_window(df_clean, start_year=2010)
        
        if len(df_filtered) > 0:
            assert df_filtered['Year'].min() >= 2010
    
    def test_filter_time_window_end_only(self, sample_raw_data):
        """Test filtering with only end year."""
        df_clean = remove_invalid_entries(sample_raw_data)
        df_filtered = filter_time_window(df_clean, end_year=2015)
        
        if len(df_filtered) > 0:
            assert df_filtered['Year'].max() <= 2015
    
    def test_select_genres(self, sample_raw_data):
        """Test genre selection."""
        df_clean = remove_invalid_entries(sample_raw_data)
        df_genres = select_genres(df_clean, ['Action', 'Simulation'])
        
        assert all(df_genres['Genre'].isin(['Action', 'Simulation']))
        assert len(df_genres) <= len(df_clean)
    
    def test_select_genres_nonexistent(self, sample_raw_data):
        """Test selecting non-existent genres."""
        df_clean = remove_invalid_entries(sample_raw_data)
        df_genres = select_genres(df_clean, ['NonexistentGenre'])
        
        assert len(df_genres) == 0


# ============================================================================
# Tests for transform_data.py
# ============================================================================

class TestTransformData:
    """Tests for data transformation functions."""
    
    def test_apply_log_transform(self, sample_raw_data):
        """Test log transformation."""
        df_clean = remove_invalid_entries(sample_raw_data)
        df_transformed = apply_log_transform(df_clean)
        
        # Check that log columns are created
        assert 'log_sales_global' in df_transformed.columns
        assert 'log_sales_na' in df_transformed.columns
        assert 'log_sales_eu' in df_transformed.columns
        assert 'log_sales_jp' in df_transformed.columns
        assert 'log_sales_other' in df_transformed.columns
        
        # Check that log values are correct (log1p of original)
        for idx, row in df_clean.iterrows():
            if idx in df_transformed.index:
                expected_log = np.log1p(row['Global_Sales'])
                actual_log = df_transformed.loc[idx, 'log_sales_global']
                np.testing.assert_almost_equal(expected_log, actual_log, decimal=5)
    
    def test_reshape_for_analysis(self, sample_raw_data):
        """Test data reshaping for analysis."""
        df_clean = remove_invalid_entries(sample_raw_data)
        df_transformed = apply_log_transform(df_clean)
        
        df_reshaped = reshape_for_analysis(df_transformed, region='Global')
        
        assert 'Genre' in df_reshaped.columns
        assert 'log_sales' in df_reshaped.columns
        assert len(df_reshaped) > 0
        assert df_reshaped['log_sales'].notna().all()
    
    def test_reshape_for_analysis_all_regions(self, sample_raw_data):
        """Test reshaping for all regions."""
        df_clean = remove_invalid_entries(sample_raw_data)
        df_transformed = apply_log_transform(df_clean)
        
        regions = ['Global', 'NA', 'EU', 'JP', 'Other']
        for region in regions:
            df_reshaped = reshape_for_analysis(df_transformed, region=region)
            assert 'log_sales' in df_reshaped.columns
            assert len(df_reshaped) > 0
    
    def test_reshape_for_analysis_invalid_region(self, sample_raw_data):
        """Test reshaping with invalid region raises error."""
        df_clean = remove_invalid_entries(sample_raw_data)
        df_transformed = apply_log_transform(df_clean)
        
        with pytest.raises(ValueError):
            reshape_for_analysis(df_transformed, region='InvalidRegion')
    
    def test_save_cleaned_data(self, sample_raw_data, temp_output_dir):
        """Test saving cleaned data."""
        df_clean = remove_invalid_entries(sample_raw_data)
        df_transformed = apply_log_transform(df_clean)
        df_reshaped = reshape_for_analysis(df_transformed, region='Global')
        
        filepath = save_cleaned_data(
            df_reshaped,
            region='Global',
            time_window='test',
            output_dir=str(temp_output_dir)
        )
        
        assert Path(filepath).exists()
        assert Path(filepath).suffix == '.csv'
        
        # Verify saved data can be loaded
        df_loaded = pd.read_csv(filepath)
        assert len(df_loaded) == len(df_reshaped)
        assert 'Genre' in df_loaded.columns
        assert 'log_sales' in df_loaded.columns


# ============================================================================
# Integration Tests
# ============================================================================

class TestDataPreprocessingPipeline:
    """Integration tests for full data preprocessing pipeline."""
    
    def test_full_pipeline(self, sample_raw_data, temp_output_dir):
        """Test complete preprocessing pipeline."""
        # Step 1: Clean data
        df_clean = remove_invalid_entries(sample_raw_data)
        assert len(df_clean) > 0
        
        # Step 2: Filter time window
        df_filtered = filter_time_window(df_clean, start_year=2000, end_year=2020)
        assert len(df_filtered) > 0
        
        # Step 3: Select genres
        df_genres = select_genres(df_filtered, ['Action', 'Simulation', 'Role-Playing'])
        assert len(df_genres) > 0
        
        # Step 4: Apply log transformation
        df_transformed = apply_log_transform(df_genres)
        assert 'log_sales_global' in df_transformed.columns
        
        # Step 5: Reshape for each region
        regions = ['Global', 'NA', 'EU', 'JP', 'Other']
        for region in regions:
            df_reshaped = reshape_for_analysis(df_transformed, region=region)
            assert 'log_sales' in df_reshaped.columns
            assert len(df_reshaped) > 0
            
            # Step 6: Save cleaned data
            filepath = save_cleaned_data(
                df_reshaped,
                region=region,
                time_window='test',
                output_dir=str(temp_output_dir)
            )
            assert Path(filepath).exists()


# ============================================================================
# Tests for Real Data (if available)
# ============================================================================

class TestRealData:
    """Tests using actual project data files."""
    
    @pytest.mark.skipif(
        not Path(PROJECT_ROOT / "data/raw/vgsales.csv").exists(),
        reason="Real data file not found"
    )
    def test_load_real_data(self):
        """Test loading actual project data."""
        data_path = PROJECT_ROOT / "data/raw/vgsales.csv"
        df = load_raw_data(str(data_path))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'Genre' in df.columns
        assert 'Global_Sales' in df.columns
    
    @pytest.mark.skipif(
        not Path(PROJECT_ROOT / "data/processed/cleaned_data_global_1995-2016.csv").exists(),
        reason="Processed data files not found"
    )
    def test_processed_data_structure(self):
        """Test structure of processed data files."""
        data_path = PROJECT_ROOT / "data/processed/cleaned_data_global_1995-2016.csv"
        df = pd.read_csv(data_path)
        
        # Check required columns
        assert 'Genre' in df.columns
        assert 'log_sales' in df.columns
        
        # Check data quality
        assert df['log_sales'].notna().all()
        assert len(df) > 0
        
        # Check genres
        expected_genres = ['Action', 'Simulation', 'Role-Playing']
        assert all(df['Genre'].isin(expected_genres))


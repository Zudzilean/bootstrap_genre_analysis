# Module Documentation

## Module 1: Data Preprocessing

### Purpose
Handle all data loading, cleaning, validation, and transformation tasks to produce standardized datasets ready for bootstrap analysis.

### Functions

#### `load_data.py`

```python
def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Load raw video game sales data from CSV file.
    
    Args:
        filepath: Path to vgsales.csv file
        
    Returns:
        DataFrame with raw data
    """
    pass

def validate_data(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Validate data integrity and completeness.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    pass
```

#### `clean_data.py`

```python
def remove_invalid_entries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with missing Genre, invalid Year, or zero sales.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    pass

def filter_time_window(df: pd.DataFrame, start_year: int = None, 
                      end_year: int = None) -> pd.DataFrame:
    """
    Filter data by release year range.
    
    Args:
        df: Input DataFrame
        start_year: Start year (inclusive)
        end_year: End year (inclusive)
        
    Returns:
        Filtered DataFrame
    """
    pass

def select_genres(df: pd.DataFrame, genres: list[str]) -> pd.DataFrame:
    """
    Filter data to include only specified genres.
    
    Args:
        df: Input DataFrame
        genres: List of genre names to include
        
    Returns:
        Filtered DataFrame
    """
    pass
```

#### `transform_data.py`

```python
def apply_log_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply log1p transformation to all sales columns.
    
    Creates new columns: log_sales_global, log_sales_na, 
    log_sales_eu, log_sales_jp, log_sales_other
    
    Args:
        df: Input DataFrame with sales columns
        
    Returns:
        DataFrame with log-transformed columns added
    """
    pass

def reshape_for_analysis(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Reshape data for bootstrap analysis by region.
    
    Args:
        df: DataFrame with log-transformed sales
        region: One of ['Global', 'NA', 'EU', 'JP', 'Other']
        
    Returns:
        DataFrame with columns: Genre, log_sales, (optional: Year, Platform)
    """
    pass

def save_cleaned_data(df: pd.DataFrame, region: str, 
                     time_window: str = 'all') -> str:
    """
    Save cleaned data to CSV file.
    
    Args:
        df: Cleaned DataFrame
        region: Region name
        time_window: Time window description (e.g., 'all', '1995-2016')
        
    Returns:
        Path to saved file
    """
    pass
```

## Module 2: Bootstrap Analysis

### Purpose
Implement bootstrap resampling procedures to estimate confidence intervals for genre means and pairwise differences.

### Functions

#### `bootstrap_means.py`

```python
def bootstrap_mean(data: np.ndarray, n_iterations: int = 10000, 
                   random_seed: int = None) -> np.ndarray:
    """
    Bootstrap resampling for mean estimation.
    
    Args:
        data: 1D array of log-transformed sales values
        n_iterations: Number of bootstrap iterations (default: 10000)
        random_seed: Random seed for reproducibility
        
    Returns:
        Array of bootstrap means
    """
    pass

def bootstrap_genre_mean_by_region(data: pd.DataFrame, genre: str, 
                                   region: str, n_iterations: int = 10000) -> dict:
    """
    Bootstrap mean for a specific genre in a specific region.
    
    Args:
        data: DataFrame with Genre and log_sales columns
        genre: Genre name
        region: Region name
        n_iterations: Number of bootstrap iterations
        
    Returns:
        Dictionary with keys: 'mean', 'bootstrap_means', 'sample_size'
    """
    pass
```

#### `bootstrap_differences.py`

```python
def bootstrap_difference(data_A: np.ndarray, data_B: np.ndarray, 
                        n_iterations: int = 10000, 
                        random_seed: int = None) -> np.ndarray:
    """
    Bootstrap resampling for difference in means.
    
    Args:
        data_A: 1D array for genre A
        data_B: 1D array for genre B
        n_iterations: Number of bootstrap iterations
        random_seed: Random seed for reproducibility
        
    Returns:
        Array of bootstrap differences (mean_A - mean_B)
    """
    pass

def bootstrap_genre_difference(data: pd.DataFrame, genre_A: str, 
                               genre_B: str, region: str, 
                               n_iterations: int = 10000) -> dict:
    """
    Bootstrap difference between two genres in a region.
    
    Args:
        data: DataFrame with Genre and log_sales columns
        genre_A: First genre name
        genre_B: Second genre name
        region: Region name
        n_iterations: Number of bootstrap iterations
        
    Returns:
        Dictionary with keys: 'mean_difference', 'bootstrap_differences', 
        'sample_size_A', 'sample_size_B'
    """
    pass
```

#### `confidence_intervals.py`

```python
def percentile_ci(bootstrap_stats: np.ndarray, confidence_level: float = 0.95) -> tuple:
    """
    Calculate percentile-based confidence interval.
    
    Args:
        bootstrap_stats: Array of bootstrap statistics
        confidence_level: Confidence level (default: 0.95)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    pass

def is_significant(ci_lower: float, ci_upper: float) -> bool:
    """
    Check if confidence interval excludes zero (significant difference).
    
    Args:
        ci_lower: Lower bound of CI
        ci_upper: Upper bound of CI
        
    Returns:
        True if CI excludes zero, False otherwise
    """
    pass
```

## Module 3: Visualization

### Purpose
Create informative visualizations of bootstrap distributions, confidence intervals, and regional comparisons.

### Functions

#### `plot_bootstrap.py`

```python
def plot_bootstrap_distribution(bootstrap_stats: np.ndarray, 
                               true_statistic: float = None,
                               ci_bounds: tuple = None,
                               title: str = None, 
                               save_path: str = None) -> None:
    """
    Plot histogram of bootstrap distribution with CI.
    
    Args:
        bootstrap_stats: Array of bootstrap statistics
        true_statistic: True/observed statistic (optional)
        ci_bounds: Tuple of (lower, upper) CI bounds (optional)
        title: Plot title
        save_path: Path to save figure (optional)
    """
    pass

def plot_genre_means_by_region(results: dict, save_path: str = None) -> None:
    """
    Plot bootstrap means for multiple genres across regions.
    
    Args:
        results: Dictionary of results keyed by (genre, region)
        save_path: Path to save figure
    """
    pass
```

#### `plot_intervals.py`

```python
def plot_confidence_intervals(results: pd.DataFrame, 
                             save_path: str = None) -> None:
    """
    Plot confidence intervals for genre means.
    
    Args:
        results: DataFrame with columns: genre, region, mean, ci_lower, ci_upper
        save_path: Path to save figure
    """
    pass
```

#### `plot_regional.py`

```python
def plot_regional_comparison(results: dict, save_path: str = None) -> None:
    """
    Create heatmap or multi-panel plot showing genre performance across regions.
    
    Args:
        results: Dictionary of results
        save_path: Path to save figure
    """
    pass

def plot_difference_distributions(results: dict, save_path: str = None) -> None:
    """
    Plot bootstrap distributions of genre differences with zero reference.
    
    Args:
        results: Dictionary of difference results
        save_path: Path to save figure
    """
    pass
```

## Module 4: Reporting

### Purpose
Generate summary tables and compile results for final report.

### Functions

#### `generate_tables.py`

```python
def create_summary_table(results: list[dict]) -> pd.DataFrame:
    """
    Create summary table of bootstrap results.
    
    Args:
        results: List of result dictionaries
        
    Returns:
        Formatted DataFrame
    """
    pass

def export_results_table(results: pd.DataFrame, filepath: str) -> None:
    """
    Export results table to CSV.
    
    Args:
        results: Results DataFrame
        filepath: Output file path
    """
    pass
```

## Usage Examples

### Complete Workflow

```python
# Step 1: Data Preprocessing (Person 1)
from src.data_preprocessing.load_data import load_raw_data
from src.data_preprocessing.clean_data import remove_invalid_entries, filter_time_window
from src.data_preprocessing.transform_data import apply_log_transform, reshape_for_analysis

df_raw = load_raw_data('data/raw/vgsales.csv')
df_clean = remove_invalid_entries(df_raw)
df_filtered = filter_time_window(df_clean, start_year=1995, end_year=2016)
df_transformed = apply_log_transform(df_filtered)
df_analysis = reshape_for_analysis(df_transformed, region='Global')

# Step 2: Bootstrap Analysis (Person 2)
from src.bootstrap_analysis.bootstrap_means import bootstrap_genre_mean_by_region
from src.bootstrap_analysis.confidence_intervals import percentile_ci, is_significant

result = bootstrap_genre_mean_by_region(df_analysis, genre='Action', region='Global')
ci_lower, ci_upper = percentile_ci(result['bootstrap_means'])

# Step 3: Visualization (Person 1)
from src.visualization.plot_bootstrap import plot_bootstrap_distribution

plot_bootstrap_distribution(
    result['bootstrap_means'],
    true_statistic=result['mean'],
    ci_bounds=(ci_lower, ci_upper),
    title='Bootstrap Distribution: Action Genre, Global Sales',
    save_path='results/figures/bootstrap_action_global.png'
)

# Step 4: Reporting (Person 2)
from src.reporting.generate_tables import create_summary_table, export_results_table

summary = create_summary_table([result])
export_results_table(summary, 'results/tables/summary_global.csv')
```


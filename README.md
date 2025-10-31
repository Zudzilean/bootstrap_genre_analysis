# Bootstrap Analysis of Genre Impact on Regional Video Game Sales

## Project Overview

This project investigates whether differences in regional sales across video game genres are statistically meaningful using bootstrap resampling techniques. We estimate 95% confidence intervals for genre-level average sales outcomes across different regions (North America, Europe, Japan, Other, and Global) and for pairwise differences between genres.

## Project Structure

```
bootstrap_genre_analysis/
├── data/                    # Data files (raw and processed)
│   ├── raw/                 # Original data files
│   └── processed/           # Cleaned and preprocessed data
├── src/                     # Source code modules
│   ├── data_preprocessing/  # Data loading and cleaning
│   ├── bootstrap_analysis/  # Bootstrap resampling functions
│   ├── visualization/       # Plotting and visualization
│   └── reporting/           # Report generation utilities
├── tests/                   # Test suite
│   ├── test_data_preprocessing.py  # Tests for data preprocessing
│   ├── conftest.py          # Shared pytest fixtures
│   └── README.md            # Test documentation
├── scripts/                 # Executable pipeline scripts
│   ├── run_preprocessing.py # Data preprocessing pipeline
│   └── README.md            # Script documentation
├── notebooks/               # Jupyter notebooks for analysis
├── results/                 # Output results
│   ├── figures/            # Generated plots and figures
│   └── tables/             # Statistical tables and summaries
└── docs/                    # Documentation
    ├── PROPOSAL.md         # Project proposal
    ├── COLLABORATION.md    # Collaboration guidelines
    └── MODULES.md          # Module documentation
```

## Module Responsibilities

### Module 1: Data Preprocessing (`src/data_preprocessing/`)
**Responsibility**: Data acquisition, cleaning, validation, and transformation
- Load raw data from CSV files
- Handle missing values and outliers
- Apply log transformations (`log1p`)
- Filter and subset data by genre, region, time period
- Export cleaned datasets for analysis

**Key Files**:
- `load_data.py`: Data loading functions
- `clean_data.py`: Data cleaning and validation
- `transform_data.py`: Log transformations and feature engineering

### Module 2: Bootstrap Analysis (`src/bootstrap_analysis/`)
**Responsibility**: Statistical analysis using bootstrap resampling
- Bootstrap resampling for genre means by region
- Bootstrap resampling for pairwise genre differences
- Confidence interval calculation (percentile method)
- Statistical significance testing
- Sensitivity analysis

**Key Files**:
- `bootstrap_means.py`: Bootstrap for genre means
- `bootstrap_differences.py`: Bootstrap for genre differences
- `confidence_intervals.py`: CI calculation and interpretation

### Module 3: Visualization (`src/visualization/`)
**Responsibility**: Creating informative plots and figures
- Bootstrap distribution plots
- Confidence interval visualizations
- Regional comparison plots
- Difference distribution plots
- Heatmaps and multi-panel figures

**Key Files**:
- `plot_bootstrap.py`: Bootstrap distribution plots
- `plot_intervals.py`: CI visualization
- `plot_regional.py`: Regional comparison plots
- `plot_utils.py`: Shared plotting utilities

### Module 4: Reporting (`src/reporting/`)
**Responsibility**: Generating reports and summaries
- Statistical summary tables
- Result compilation
- Report template generation

**Key Files**:
- `generate_tables.py`: Summary table generation

## Collaboration Strategy

### Work Assignment

**Person 1 Responsibilities:**
- ✅ Module 1: Data Preprocessing (CODE COMPLETE - ready for testing)
- ✅ Module 3: Visualization (CODE COMPLETE - ready for use)
- See `PERSON1_STATUS.md` for detailed task list

**Person 2 Responsibilities:**
- ⚠️ Module 2: Bootstrap Analysis (TEMPLATE PROVIDED - needs testing and implementation)
- ⚠️ Module 4: Reporting (TEMPLATE PROVIDED - needs completion)
- See `PERSON2_STATUS.md` for detailed task list and TODO checklist

### Workflow
1. **Data Preprocessing** (Person 1): Prepares clean, standardized datasets
2. **Bootstrap Analysis** (Person 2): Uses cleaned data to perform statistical analysis
3. **Visualization** (Person 1): Creates figures based on analysis results
4. **Reporting** (Person 2): Compiles results and generates final report

### Interface Contracts
- **Data → Analysis**: Cleaned CSV files with standardized column names
- **Analysis → Visualization**: Results dictionaries/DataFrames with consistent structure
- **Visualization → Reporting**: Saved figure files and metadata

### Status Tracking
- **Person 1 Status**: See `PERSON1_STATUS.md`
- **Person 2 Status**: See `PERSON2_STATUS.md` (includes complete TODO list)

See `docs/COLLABORATION.md` for detailed collaboration guidelines.

## Getting Started

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy jupyter
```

### Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Place raw data files in `data/raw/` (e.g., `vgsales.csv`)
3. Run tests: `pytest tests/` (optional, but recommended)
4. Run data preprocessing: `python scripts/run_preprocessing.py`
5. Run bootstrap analysis: See `scripts/` for analysis scripts (Person 2)
6. Generate visualizations: See `scripts/` for visualization scripts (Person 1)
7. Compile report: See reporting module

### Testing

Run the test suite to verify all modules work correctly:

```bash
# Run all tests (recommended for Windows/PowerShell)
python -m pytest tests/

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test module
python -m pytest tests/test_data_preprocessing.py
```

**Note**: On Windows/PowerShell, use `python -m pytest` instead of `pytest` if the command is not recognized.

See `tests/README.md` for detailed testing documentation.

## Key Parameters

- **Bootstrap iterations**: B = 10,000
- **Confidence level**: 95% (α = 0.05)
- **Log transformation**: `log1p()` for all sales metrics
- **Regions**: Global, NA, EU, JP, Other
- **Time window**: 1995-2016 (optional sensitivity: all years)

## Expected Deliverables

1. **Jupyter Notebook**: End-to-end analysis workflow
2. **Visualizations**: Bootstrap distributions, CI plots, regional comparisons
3. **Scientific Report**: 8-10 page professional report
4. **Reproducible Code**: All source code with documentation

## References

- Elements of Data Science, Chapters 10 and 12
- Efron & Tibshirani, An Introduction to the Bootstrap
- Kaggle Video Game Sales dataset


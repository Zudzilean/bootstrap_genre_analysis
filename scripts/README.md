# Scripts Directory

This directory contains executable scripts for running the analysis pipeline.

## Scripts

### `run_preprocessing.py`
**Person 1 - Data Preprocessing Pipeline**

Runs the complete data preprocessing workflow:
1. Loads raw data from `data/raw/vgsales.csv`
2. Validates data integrity
3. Removes invalid entries (missing Genre, invalid Year, zero sales)
4. Filters time window to 1995-2016
5. Selects genres: Action, Simulation, Role-Playing
6. Applies log transformations (`log1p`)
7. Reshapes data for each region
8. Saves cleaned data to `data/processed/`

**Usage:**
```bash
# From project root directory
python scripts/run_preprocessing.py
```

**Output:**
- Creates 5 CSV files in `data/processed/`:
  - `cleaned_data_global_1995-2016.csv`
  - `cleaned_data_na_1995-2016.csv`
  - `cleaned_data_eu_1995-2016.csv`
  - `cleaned_data_jp_1995-2016.csv`
  - `cleaned_data_other_1995-2016.csv`

**Prerequisites:**
- Raw data file must exist at `data/raw/vgsales.csv`
- All dependencies installed (`pip install -r requirements.txt`)

---

## Adding New Scripts

When adding new scripts to this directory:

1. **Naming convention**: Use descriptive names with underscores (e.g., `run_bootstrap_analysis.py`)
2. **Path handling**: Always use `Path(__file__).parent.parent` to get project root for relative paths
3. **Documentation**: Add a header docstring and update this README
4. **Working directory**: Scripts should change to project root at start (see `run_preprocessing.py` for example)

### `run_bootstrap_analysis.py`
**Bootstrap Analysis Pipeline**

Runs the complete bootstrap analysis workflow:
1. Loads cleaned data for each region
2. Runs bootstrap for genre means (all genres × all regions, N=10,000)
3. Runs bootstrap for genre differences (all pairs × all regions, N=10,000)
4. Calculates 95% confidence intervals and significance tests
5. Saves results to `results/tables/`

**Usage:**
```bash
# From project root directory
python scripts/run_bootstrap_analysis.py
```

**Output:**
- Creates CSV files in `results/tables/`:
  - `bootstrap_means_all_regions.csv` - All genre means
  - `bootstrap_differences_all_regions.csv` - All genre differences
  - `bootstrap_means_[region].csv` - Means by region
  - `bootstrap_differences_[region].csv` - Differences by region

**Prerequisites:**
- Cleaned data files in `data/processed/`
- All dependencies installed

---

### `generate_figures.py`
**Figure Generation Pipeline**

Generates all required visualizations from bootstrap results:
1. Bootstrap distribution plots for each genre-region combination
2. Confidence interval plots for genre means
3. Regional comparison heatmaps
4. Genre means comparison bar charts
5. Difference distribution plots with zero reference

**Usage:**
```bash
# From project root directory
python scripts/generate_figures.py
```

**Output:**
- Creates PNG files in `results/figures/` (300 DPI):
  - `bootstrap_dist_[genre]_[region].png` - Bootstrap distributions
  - `confidence_intervals_[region].png` - CI plots
  - `confidence_intervals_all_regions.png` - Combined CI plot
  - `regional_comparison_heatmap.png` - Regional heatmap
  - `genre_means_by_region.png` - Means comparison
  - `difference_distributions_[region].png` - Difference distributions

**Prerequisites:**
- Bootstrap analysis results in `results/tables/`
- All dependencies installed

---

## Script Organization

- **Preprocessing scripts**: `run_preprocessing.py`
- **Analysis scripts**: `run_bootstrap_analysis.py`
- **Visualization scripts**: `generate_figures.py`
- **Utility scripts**: General helper scripts for the project


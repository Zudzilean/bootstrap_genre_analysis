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

## Script Organization

- **Preprocessing scripts**: `run_preprocessing.py` (Person 1)
- **Analysis scripts**: TBD (Person 2 - bootstrap analysis)
- **Visualization scripts**: TBD (Person 1 - after analysis)
- **Utility scripts**: General helper scripts for the project


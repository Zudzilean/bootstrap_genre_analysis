# Collaboration Guidelines

## Module Independence

Each module is designed to be worked on independently, with clear interfaces between modules.

## Work Allocation

### Person 1: Data Pipeline & Visualization
**Modules**: 
- `src/data_preprocessing/` (Data loading, cleaning, transformation)
- `src/visualization/` (All plotting functions)

**Deliverables**:
- Clean, validated datasets in `data/processed/`
- Standardized data format documentation
- All visualization functions and figure outputs

**Workflow**:
1. Start with data preprocessing module
2. Create cleaned datasets and document the data schema
3. After Person 2 completes analysis, create visualizations using their results
4. Save all figures to `results/figures/`

### Person 2: Statistical Analysis & Reporting
**Modules**:
- `src/bootstrap_analysis/` (All bootstrap functions)
- `src/reporting/` (Report generation)

**Deliverables**:
- Bootstrap analysis functions
- Statistical results (CIs, p-values, etc.)
- Final report compilation

**Workflow**:
1. Wait for Person 1 to provide cleaned data
2. Implement bootstrap functions
3. Run analysis and save results to `results/tables/`
4. Generate final report using Person 1's figures

## Interface Specifications

### Data Format (Output from `data_preprocessing/`)

Cleaned data should be saved as CSV files with the following columns:
- `Genre`: Game genre (string)
- `Region`: One of ['Global', 'NA', 'EU', 'JP', 'Other']
- `log_sales`: Log-transformed sales (`log1p(sales)`)
- `Year`: Release year (optional, for time window filtering)
- `Platform`: Platform name (optional, for sensitivity analysis)

**File naming convention**: `cleaned_data_[region]_[timewindow].csv`

**Example**: `cleaned_data_global_all.csv`, `cleaned_data_na_1995-2016.csv`

### Analysis Results Format (Output from `bootstrap_analysis/`)

Results should be saved as JSON or CSV with the following structure:

**For genre means**:
```json
{
  "region": "Global",
  "genre": "Action",
  "mean": 2.34,
  "ci_lower": 2.12,
  "ci_upper": 2.56,
  "sample_size": 150
}
```

**For genre differences**:
```json
{
  "region": "Global",
  "genre_A": "Action",
  "genre_B": "Simulation",
  "mean_difference": 0.45,
  "ci_lower": 0.23,
  "ci_upper": 0.67,
  "significant": true,
  "sample_size_A": 150,
  "sample_size_B": 120
}
```

**File naming convention**: 
- `bootstrap_means_[region].csv`
- `bootstrap_differences_[region].csv`

### Visualization Input Format

Visualization functions should accept:
- DataFrames with standardized column names
- Result dictionaries/JSON files from bootstrap analysis
- Configuration dictionaries for plot customization

## Communication Protocol

### Weekly Checkpoints
- **Week 1**: Person 1 completes data preprocessing; Person 2 reviews data format
- **Week 2**: Person 2 completes bootstrap analysis; Person 1 reviews results format
- **Week 3**: Person 1 completes visualizations; Person 2 integrates into report
- **Week 4**: Final integration and review

### Git Workflow (if using version control)
- Work on separate branches: `feature/data-preprocessing` and `feature/bootstrap-analysis`
- Merge to `main` after module completion and testing
- Use pull requests for code review

### File Naming Conventions
- All Python files: `snake_case.py`
- All data files: `descriptive_name_version.csv`
- All figure files: `figure_name_region_genre.png`
- All result files: `results_type_region.csv`

## Testing and Validation

### Person 1 (Data Preprocessing)
- Verify data types and ranges
- Check for missing values
- Validate log transformations
- Create data summary statistics

### Person 2 (Bootstrap Analysis)
- Test bootstrap functions with known distributions
- Validate confidence intervals (coverage properties)
- Cross-check with reference parametric tests
- Document any assumptions or limitations

## Conflict Resolution

If interface changes are needed:
1. Document required changes
2. Update this COLLABORATION.md file
3. Notify the other person immediately
4. Agree on new interface before implementation

## Code Standards

- **Documentation**: All functions must have docstrings (Google style)
- **Comments**: Explain complex logic, especially statistical procedures
- **Style**: Follow PEP 8 for Python code
- **Language**: All code and comments in English

## Dependencies

### Shared Dependencies
- pandas >= 1.3.0
- numpy >= 1.20.0
- matplotlib >= 3.3.0
- seaborn >= 0.11.0

### Person 1 Specific
- (Data preprocessing may require additional libraries)

### Person 2 Specific
- scipy >= 1.7.0 (for reference statistical tests)

## Common Issues and Solutions

### Issue: Data format mismatch
**Solution**: Check `docs/COLLABORATION.md` interface specifications, use data validation functions

### Issue: Missing intermediate files
**Solution**: Ensure all files follow naming conventions, check `data/processed/` directory

### Issue: Figure format not compatible
**Solution**: Standardize on PNG format with 300 DPI for figures


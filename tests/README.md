# Test Suite

This directory contains unit tests and integration tests for the bootstrap genre analysis project.

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── test_data_preprocessing.py     # Tests for data preprocessing module
├── test_bootstrap_analysis.py     # Tests for bootstrap analysis (Person 2)
├── test_visualization.py          # Tests for visualization module
└── README.md                      # This file
```

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements.txt  # Includes pytest
```

**Note for Windows/PowerShell users**: If `pytest` command is not recognized, use `python -m pytest` instead.

### Run All Tests

From project root:
```bash
# Recommended: Use python -m pytest (works on all platforms)
python -m pytest tests/

# Alternative: Direct pytest command (if available in PATH)
pytest tests/
```

### Run Specific Test Module

```bash
# Test data preprocessing
python -m pytest tests/test_data_preprocessing.py

# Test specific class
python -m pytest tests/test_data_preprocessing.py::TestLoadData

# Test specific function
python -m pytest tests/test_data_preprocessing.py::TestLoadData::test_load_raw_data_success
```

### Run with Verbose Output

```bash
python -m pytest tests/ -v
```

### Run with Coverage Report

```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Run Tests in Parallel (faster)

```bash
python -m pytest tests/ -n auto
```

### Windows PowerShell Users

If you encounter "pytest is not recognized", always use:
```powershell
python -m pytest tests/
```

This uses Python's module execution and works regardless of PATH configuration.

## Test Categories

### Unit Tests

Test individual functions in isolation:
- `test_data_preprocessing.py`: Tests for load, clean, transform functions

### Integration Tests

Test complete workflows:
- `TestDataPreprocessingPipeline`: Full preprocessing pipeline

### Real Data Tests

Tests using actual project data (marked with `@pytest.mark.skipif` if data unavailable):
- `TestRealData`: Tests with actual CSV files

## Writing New Tests

### For Person 1

Add tests to `test_data_preprocessing.py` or `test_visualization.py`:

```python
def test_my_new_function():
    """Test description."""
    # Arrange
    input_data = ...
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == expected_output
```

### For Person 2

Create `test_bootstrap_analysis.py`:

```python
import pytest
from src.bootstrap_analysis.bootstrap_means import bootstrap_mean

def test_bootstrap_mean():
    """Test bootstrap mean calculation."""
    data = np.array([1, 2, 3, 4, 5])
    result = bootstrap_mean(data, n_iterations=1000, random_seed=42)
    assert len(result) == 1000
    assert result.mean() == pytest.approx(data.mean(), abs=0.5)
```

## Test Best Practices

1. **Naming**: Test functions should start with `test_`
2. **Isolation**: Each test should be independent
3. **Fixtures**: Use pytest fixtures for reusable test data
4. **Assertions**: Use descriptive assertions with clear error messages
5. **Coverage**: Aim for high code coverage (>80%)
6. **Fast**: Tests should run quickly (<1 minute total)

## Continuous Integration

Tests should be run:
- Before committing code
- In CI/CD pipeline (if set up)
- Before merging pull requests

## Troubleshooting

### Import Errors

If tests fail with import errors:
1. Ensure you're running from project root
2. Check that `src/` is in Python path
3. Verify `__init__.py` files exist in all packages

### Missing Dependencies

Install all required packages:
```bash
pip install -r requirements.txt
```

### Real Data Tests Skipped

Some tests are skipped if data files don't exist. This is expected if:
- Data preprocessing hasn't been run yet
- Test data files are in a different location

To run these tests, ensure data files exist or update the `@pytest.mark.skipif` conditions.


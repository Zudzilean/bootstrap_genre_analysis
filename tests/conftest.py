"""
Pytest configuration and shared fixtures.

This file is automatically discovered by pytest and provides
fixtures available to all test modules.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

@pytest.fixture(scope="session")
def project_root():
    """Return project root directory."""
    return PROJECT_ROOT

@pytest.fixture
def sample_dataframe():
    """Create a minimal valid sample DataFrame for testing."""
    return pd.DataFrame({
        'Name': ['TestGame1', 'TestGame2'],
        'Platform': ['PS4', 'Xbox'],
        'Year': [2010.0, 2015.0],
        'Genre': ['Action', 'Simulation'],
        'Publisher': ['TestPub1', 'TestPub2'],
        'NA_Sales': [1.0, 1.5],
        'EU_Sales': [0.8, 1.2],
        'JP_Sales': [0.3, 0.2],
        'Other_Sales': [0.2, 0.3],
        'Global_Sales': [2.3, 3.2]
    })


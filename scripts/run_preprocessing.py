"""
Data Preprocessing Pipeline Script

This script runs the complete data preprocessing pipeline:
1. Load raw data
2. Validate data
3. Clean data (remove invalid entries)
4. Filter time window (1995-2016)
5. Select genres (Action, Simulation, Role-Playing)
6. Apply log transformations
7. Reshape for each region
8. Save cleaned data

Usage:
    From project root: python scripts/run_preprocessing.py
    Or from scripts/: python run_preprocessing.py (when run from project root)
"""

import sys
from pathlib import Path

# Get project root directory (parent of scripts/)
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

def main():
    """Run the complete data preprocessing pipeline."""
    
    # Change to project root for relative paths to work correctly
    import os
    original_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)
    
    try:
        print("=" * 60)
        print("Data Preprocessing Pipeline")
        print("=" * 60)
        
        # Step 1: Load raw data
        print("\n[1/7] Loading raw data...")
        raw_data_path = "data/raw/vgsales.csv"
        df_raw = load_raw_data(raw_data_path)
        print(f"Loaded {len(df_raw)} rows")
        print(f"Columns: {list(df_raw.columns)}")
        
        # Step 2: Validate data
        print("\n[2/7] Validating data...")
        is_valid, issues = validate_data(df_raw)
        if not is_valid:
            print("Validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("[OK] Data validation passed")
        
        # Step 3: Clean data
        print("\n[3/7] Cleaning data (removing invalid entries)...")
        df_clean = remove_invalid_entries(df_raw)
        print(f"After cleaning: {len(df_clean)} rows")
        
        # Step 4: Filter time window (1995-2016)
        print("\n[4/7] Filtering time window (1995-2016)...")
        df_filtered = filter_time_window(df_clean, start_year=1995, end_year=2016)
        print(f"After time filtering: {len(df_filtered)} rows")
        print(f"Year range: {df_filtered['Year'].min():.0f} - {df_filtered['Year'].max():.0f}")
        
        # Step 5: Select genres (Action, Simulation, Role-Playing)
        print("\n[5/7] Selecting genres (Action, Simulation, Role-Playing)...")
        selected_genres = ['Action', 'Simulation', 'Role-Playing']
        df_genres = select_genres(df_filtered, selected_genres)
        print(f"After genre filtering: {len(df_genres)} rows")
        print(f"Genres distribution:")
        print(df_genres['Genre'].value_counts())
        
        # Step 6: Apply log transformations
        print("\n[6/7] Applying log transformations...")
        df_transformed = apply_log_transform(df_genres)
        print("[OK] Log transformations applied")
        log_cols = [col for col in df_transformed.columns if col.startswith('log_sales')]
        print(f"Created log columns: {log_cols}")
        
        # Step 7: Reshape and save for each region
        print("\n[7/7] Reshaping data for each region and saving...")
        regions = ['Global', 'NA', 'EU', 'JP', 'Other']
        time_window = '1995-2016'
        
        saved_files = []
        for region in regions:
            print(f"\n  Processing region: {region}")
            df_reshaped = reshape_for_analysis(df_transformed, region=region)
            print(f"    Shape: {df_reshaped.shape}")
            print(f"    Genres: {df_reshaped['Genre'].unique()}")
            
            # Save cleaned data
            filepath = save_cleaned_data(
                df_reshaped, 
                region=region, 
                time_window=time_window,
                output_dir='data/processed'
            )
            saved_files.append(filepath)
        
        print("\n" + "=" * 60)
        print("Data Preprocessing Complete!")
        print("=" * 60)
        print(f"\nSaved {len(saved_files)} files to data/processed/:")
        for filepath in saved_files:
            print(f"  - {Path(filepath).name}")
        print("\nNext steps:")
        print("  1. Person 2 will use these files for bootstrap analysis")
        print("  2. After Person 2 completes, create visualizations")
        
        return saved_files
    
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

if __name__ == "__main__":
    main()


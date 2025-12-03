"""
Reporting Module

This module provides functions for generating summary tables and reports.
"""

from .generate_tables import (
    create_summary_table,
    export_results_table,
    format_number,
    make_latex_table,
    region_specific_tables,
    genre_comparison_matrix
)

__all__ = [
    'create_summary_table',
    'export_results_table',
    'format_number',
    'make_latex_table',
    'region_specific_tables',
    'genre_comparison_matrix'
]


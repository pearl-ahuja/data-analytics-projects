# Data Preparation

## Overview

This stage prepares the Olist Brazilian E-Commerce data for analysis using Microsoft Excel and Power Query.

The objective is to understand the structure and quality of the source data, standardize inconsistent values where appropriate, and prepare the datasets for import into MySQL.

## Work Performed

- Reviewed table structures, column names, data types, and distinct values.
- Used Power Query profiling features to inspect column quality, distribution, and completeness.
- Trimmed unnecessary whitespace in selected text columns.
- Investigated missing values, blank product categories, zero-valued payments or freight charges, and unusual payment installments.
- Removed exact duplicate rows from the geolocation dataset.
- Preserved meaningful missing values instead of replacing them without justification.
- Created a data dictionary describing the tables and their columns.
- Prepared cleaned CSV files for SQL analysis.

## Data Quality Principles

Not every unusual value is automatically an error. Missing values, zero amounts, and incomplete records were considered in context before deciding how to handle them.

For example, missing product dimensions or weights were not automatically replaced with averages, because doing so could introduce unsupported assumptions.

## Deliverables

- Cleaned datasets prepared for SQL import.
- Data dictionary documenting tables and columns.
- Supporting cleaning documentation, where available.

## Next Stage

The prepared datasets are imported into MySQL for validation and analytical querying. See [`02_SQL_Analysis`](../02_SQL_Analysis/).

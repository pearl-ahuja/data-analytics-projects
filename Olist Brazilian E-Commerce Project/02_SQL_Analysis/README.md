# SQL Analysis

## Overview

This stage uses MySQL to validate the prepared datasets, establish relationships between tables, and answer business questions through SQL queries.

## Database

- **DBMS:** MySQL
- **Database name:** `olist_ecommerce`

The imported tables were checked against the prepared datasets to verify record counts.

## Topics Covered

The SQL scripts cover:

- Basic queries, filtering, and sorting
- Aggregate functions and grouping
- INNER JOIN and LEFT JOIN
- CASE statements
- Common Table Expressions (CTEs)
- Subqueries
- Window functions and ranking
- Date and other useful SQL functions
- Mixed business-oriented problems
- Data import and database preparation

## Business Questions

The analysis explores questions such as:

- Which product categories and sellers generate the highest item-price revenue?
- How do order volumes and revenue vary over time?
- Which customer states contribute the most orders?
- Which payment methods account for the largest payment values?
- How are review scores distributed?
- Which categories and sellers perform best under selected metrics?

## Database Relationships

The EER diagram illustrates the database structure and relationships between the tables. Refer to the diagram included in this folder.

## How to Use

1. Set up MySQL and create or select the `olist_ecommerce` database.
2. Ensure the required tables have been imported.
3. Open the SQL scripts in MySQL Workbench.
4. Execute the relevant queries against the database.

Some scripts are intended for initial data import and setup, while others perform analysis. Review a script before running it, particularly if it contains file paths or table-creation statements.

## Interpretation Notes

- Revenue calculated from `order_items.price` represents item-price revenue, not total payment value.
- Reviews are associated with orders. Category-level review analysis can be affected when an order contains products from multiple categories.

The scripts are organized to demonstrate SQL development from basic operations to more advanced analytical queries.

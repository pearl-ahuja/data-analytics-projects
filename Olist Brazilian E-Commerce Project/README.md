# Olist Brazilian E-Commerce Data Analysis

An end-to-end data analytics project exploring Brazilian e-commerce order data to understand sales performance, customer behavior, delivery efficiency, and customer satisfaction.

## Project Overview

This project analyzes the Olist Brazilian E-Commerce dataset using Excel, MySQL, and Power BI. The workflow covers data profiling and cleaning, SQL-based analysis, and interactive dashboard development.

The objective is to transform raw transactional data into meaningful insights that can help identify business performance trends and areas for improvement.

## Business Objectives

- Analyze revenue, order volume, and average order value.
- Identify top-performing product categories and sellers.
- Understand customer distribution across Brazilian states.
- Evaluate order processing, shipping, and delivery performance.
- Analyze customer review scores and satisfaction patterns.
- Identify opportunities to improve operational efficiency and customer experience.

## Tools and Technologies

- **Microsoft Excel / Power Query:** Data profiling, cleaning, and preparation.
- **MySQL:** Data storage, querying, joins, aggregations, CTEs, subqueries, and window functions.
- **Power BI:** KPI development, interactive visualizations, and dashboard reporting.
- **GitHub:** Project documentation, version control, and portfolio presentation.

## Project Workflow

1. **Data Preparation:** Profile and clean the raw datasets, investigate data-quality issues, and document the tables and columns.
2. **SQL Analysis:** Import the prepared data into MySQL, validate table records and relationships, and write analytical queries.
3. **Power BI Dashboard:** Build an interactive dashboard to explore sales, delivery performance, and customer ratings.
4. **Documentation:** Maintain the data dictionary, SQL scripts, dashboard export, and project presentation.

## Dashboard Overview

The Power BI dashboard contains three analytical pages:

### 1. Main Dashboard
- Total revenue
- Total orders
- Average order value
- Total customers
- Product category and monthly sales analysis

### 2. Delivery Performance
- Late deliveries and dispatch delays
- Order processing time
- Shipping and delivery duration
- Relationship between order price and delivery time

### 3. Product Ratings
- Total reviews and average review score
- Five-star and low-rating reviews
- Highest- and lowest-rated product categories
- Review score distribution

The dashboard PDF is available in [`03_PowerBI_Dashboard`](03_PowerBI_Dashboard/).

## Key Dashboard Metrics

The current dashboard displays approximately:

| Metric | Value |
|---|---:|
| Total Revenue | 13.59M |
| Total Orders | 99K |
| Average Order Value | 136.68 |
| Total Customers | 96K |
| Average Review Score | 4.09 |

*These figures reflect the current dashboard and its calculation definitions. Revenue is calculated using order-item prices; it should not be interpreted as total payment value.*

## Repository Structure

- [`01_Data_Preparation`](01_Data_Preparation/) — Data preparation documentation and data dictionary.
- [`02_SQL_Analysis`](02_SQL_Analysis/) — SQL scripts and database relationship diagram.
- [`03_PowerBI_Dashboard`](03_PowerBI_Dashboard/) — Dashboard PDF and related files.
- [`04_Project_Presentation`](04_Project_Presentation/) — Project overview presentation.
- [`data`](data/) — Dataset source and data availability information.

## Dataset

The project uses the Olist Brazilian E-Commerce dataset, which contains information about orders, customers, products, sellers, payments, reviews, and related entities.

Refer to [`data/README.md`](data/README.md) for dataset information and access details.

## Notes

- Data cleaning decisions are documented rather than automatically replacing every missing or unusual value.
- SQL scripts demonstrate both query development and business-oriented analysis.
- The dashboard PDF provides a viewable preview; the editable Power BI file is not currently included in this repository.

## Author

**Pearl Ahuja**

This project demonstrates an end-to-end analytics workflow, from data preparation and SQL analysis to dashboard development and documentation.

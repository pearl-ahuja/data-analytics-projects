# Project: Olist Brazilian E-Commerce Data Analysis (end-to-end)

Author's workflow, in order:
1. Raw data: Olist public Brazilian e-commerce dataset (9 tables, ~100K orders, Sep 2016 - Oct 2018).
2. Cleaning in Excel / Power Query: trimmed spaces, checked duplicates, nulls, primary keys, data types and date formats; documented every check in a cleaning log (one sheet per table).
3. Database in MySQL: tables loaded, primary/foreign keys added, EER diagram designed in MySQL Workbench; analysis written in SQL using joins, CTEs and window functions.
4. Dashboard in Power BI: 3 pages - Main Dashboard (revenue, orders, AOV, customers, review score, best-selling categories, monthly sales), Delivery Performance (late deliveries, processing/shipping times, order status map, price vs delivery time), Product Ratings (review distribution, top/least rated categories).
5. This chatbot: lets anyone ask free-form questions. It converts the question to SQL, runs it on the same cleaned data (loaded into DuckDB for hosting), and explains the result.

Cleaning log highlights (from the project's cleaning_log.xlsx):
- customers: 99,441 rows, no nulls/duplicates; customer_unique_id repeats are expected (repeat buyers).
- orders: 99,441 rows; nulls exist in the delivery timestamps (orders not yet delivered / cancelled) - investigated and documented; some inconsistencies between order status and delivered date were documented.
- products: 32,951 rows; missing metadata (category, dimensions) for a small subset - documented; product_category_name translated to English via a translation table.
- order_items: 112,650 rows; composite primary key (order_id, order_item_id) validated; no price = 0; some freight_value = 0.
- order_payments: 103,886 rows; payment_type 'not_defined' only appears with zero payment value; some zero-value voucher payments; two credit-card rows with 0 installments but non-zero value were retained as possible business exceptions.

Dashboard headline numbers (all-time, no filters):
- Total revenue 13.59M BRL (sum of item price, freight excluded); total orders ~99K; AOV 136.68 (revenue / orders); ~96K unique customers; average review score 4.09.
- Review counts: 99.22K total, 57.33K five-star, 11.42K one-star, 14.57K "bad" reviews (score 1 or 2).
- Delivery: ~8K orders delivered after the estimated date.
- Top categories by revenue: health_beauty, watches_gifts, bed_bath_table, sports_leisure, computers_accessories.
- Sales peak in November 2017 (Black Friday period).
- Highest rated categories include cds_dvds_musicals, fashion_childrens_clothes, books_general_interest; lowest rated include security_and_services, office_furniture, fashion_male_clothing.

Metric definitions used by the chatbot (kept consistent with the dashboard):
- Revenue = SUM(order_items.price). Freight is NOT included. Payment value (order_payments.payment_value) is a different, larger number (~16.0M) because it includes freight.
- Orders = COUNT(DISTINCT order_id) from orders (all statuses unless the user asks otherwise).
- AOV = revenue / number of orders.
- Customers = COUNT(DISTINCT customer_unique_id).
- Late delivery = order_delivered_customer_date > order_estimated_delivery_date.
- Delivery time (days) = order_delivered_customer_date - order_purchase_timestamp.
- Bad review = review_score <= 2.

#Find the top 5 product categories by revenue and
#show their percentage contribution to total Olist revenue.

WITH category_revenue AS (
SELECT p.product_category_name, SUM(oi.price) AS revenue 
FROM products as p
INNER JOIN
order_items AS oi
ON p.product_id = oi.product_id
GROUP BY p.product_category_name
)
SELECT 
	product_category_name, revenue, revenue*100/SUM(revenue) OVER () AS percent_contribution
FROM top_categories
ORDER BY revenue DESC
LIMIT 5;




#For each month, find the top-selling product category by revenue,
#along with its revenue and its percentage of that month's total revenue.

WITH monthly_cat_revenue AS(
SELECT 
	DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month, 
    p.product_category_name,
    SUM(oi.price) AS revenue
FROM 
	orders AS o
INNER JOIN
	order_items AS oi
ON 
	o.order_id = oi.order_id
INNER JOIN 
	products AS p
ON 
	p.product_id = oi.product_id
GROUP BY
	p.product_category_name, DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') ),

category_revenue_monthly AS (
SELECT *,
	revenue*100/ SUM(revenue) OVER(PARTITION BY month) AS percentage_revenue
FROM monthly_cat_revenue
),

ranked_categories AS(
SELECT *, 
	ROW_NUMBER() OVER(
    PARTITION BY month
    ORDER BY revenue DESC) AS rn
FROM category_revenue_monthly)

SELECT month, product_category_name, revenue, percentage_revenue
FROM ranked_categories 
WHERE rn = 1;
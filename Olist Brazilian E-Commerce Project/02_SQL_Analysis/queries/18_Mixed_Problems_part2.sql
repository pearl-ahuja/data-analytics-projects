WITH monthly_revenue AS(
SELECT
	DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    SUM(oi.price) AS revenue
FROM orders AS o
INNER JOIN order_items AS oi
ON o.order_id = oi.order_id
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')),

mom_revenue AS (
SELECT 
	month, revenue,
    LAG(revenue) OVER(
    ORDER BY month
    ) AS previous_month_revenue
    FROM monthly_revenue
)
SELECT month, revenue, previous_month_revenue, (revenue-previous_month_revenue) AS growth
FROM mom_revenue;


SELECT *,
	SUM(revenue) OVER(
    ORDER BY month)
    AS running_revenue
FROM monthly_revenue

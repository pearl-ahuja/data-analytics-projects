#Top 3 sellers by revenue within each customer state,
#among sellers whose overall seller revenue is above average.

WITH seller_revenue AS
(
	SELECT seller_id, SUM(price) AS revenue
    FROM order_items
    GROUP BY seller_id
),
high_sellers AS
(
SELECT seller_id, revenue
FROM seller_revenue
WHERE revenue > (
	SELECT AVG(revenue)
    FROM seller_revenue
    )
),
state_dist AS 
(
SELECT c.customer_state, oi.seller_id, SUM(oi.price) AS revenue
FROM customers AS c
INNER JOIN orders AS o
ON c.customer_id = o.customer_id
INNER JOIN order_items AS oi
ON o.order_id = oi.order_id
WHERE oi.seller_id IN (
        SELECT seller_id
        FROM high_sellers
    )
    GROUP BY c.customer_state, oi.seller_id
),
row_num as (
SELECT customer_state,
        seller_id,
        revenue, 
	ROW_NUMBER() OVER(
    PARTITION BY customer_state
	ORDER BY revenue DESC)
    AS rn
FROM state_dist
)
SELECT * FROM row_num
WHERE rn<=3 

SELECT c.customer_id, o.order_id
FROM customers AS c
LEFT JOIN
orders AS o
ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

SELECT p.product_id, oi.order_id
FROM products AS p
LEFT JOIN
order_items AS oi
ON p.product_id = oi.product_id
WHERE oi.order_id IS NULL;

SELECT o.order_id, r.review_id
FROM orders AS o
LEFT JOIN order_reviews AS r
ON o.order_id = r.order_id
WHERE r.review_id IS NULL;
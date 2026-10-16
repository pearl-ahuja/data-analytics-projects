SELECT order_id, o.customer_id, c.customer_city, c.customer_state
FROM orders AS o
INNER JOIN 
customers AS c
ON o.customer_id = c.customer_id;


SELECT oi.order_id, oi.product_id, p.product_category_name, oi.price, o.order_id, o.customer_id, c.customer_city
FROM order_items AS oi
INNER JOIN
products AS p
ON o.product_id = p.product_id;


SELECT c.customer_city, c.customer_state, o.order_id, op.payment_value, op.payment_type
FROM customers AS c
INNER JOIN
orders AS o
ON o.customer_id = c.customer_id
INNER JOIN
order_payments AS op
ON o.order_id = op.order_id;


SELECT s.seller_id, s.seller_state, oi.product_id, oi.price
FROM sellers AS s
INNER JOIN 
order_items AS oi
ON oi.seller_id = s.seller_id;


SELECT r.review_id, r.review_score, c.customer_city, p.product_category_name
FROM order_reviews AS r
INNER JOIN
orders AS o
ON r.order_id = o.order_id
INNER JOIN
customers as c
ON c.customer_id = o.customer_id
INNER JOIN 
order_items AS oi
ON oi.order_id = o.order_id
INNER JOIN
products AS p
ON p.product_id = oi.product_id;
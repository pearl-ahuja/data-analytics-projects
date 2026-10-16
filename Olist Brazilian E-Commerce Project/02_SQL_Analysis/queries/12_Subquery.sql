SELECT c.customer_unique_id, SUM(op.payment_value) as total_spending
FROM order_payments  AS op
INNER JOIN orders AS o 
ON o.order_id = op.order_id
INNER JOIN customers AS c
ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
HAVING 
total_spending > (
SELECT AVG(total_spending) FROM
(SELECT c.customer_unique_id, SUM(op.payment_value) as total_spending
FROM order_payments  AS op
INNER JOIN orders AS o 
ON o.order_id = op.order_id
INNER JOIN customers AS c
ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id)
 as customer_spending);

SELECT *
FROM orders
WHERE customer_id IN
(
    SELECT customer_id
    FROM customers
    WHERE customer_state = 'RJ'
);

SELECT *
FROM order_payments
WHERE order_id IN
(
    SELECT order_id
    FROM orders
    WHERE order_status = 'delivered'
);

SELECT *
FROM order_reviews
WHERE order_id IN
(
    SELECT order_id
    FROM orders
    WHERE order_status = 'cancelled'
);


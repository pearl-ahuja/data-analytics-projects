WITH ov AS
(SELECT 
	oi.order_id as orderID, SUM(oi.price) AS order_value
FROM
	order_items AS oi
GROUP BY 
	oi.order_id)
    
SELECT c.customer_state, AVG(ov.order_value)
FROM customers AS c
INNER JOIN
orders AS o 
ON c.customer_id = o.customer_id
INNER JOIN 
ov 
ON ov.orderID = o.order_id
GROUP BY
c.customer_state;



WITH slrs as
(SELECT seller_id , AVG(price) AS avg_price
FROM order_items
GROUP BY seller_id)

SELECT seller_id, avg_price,
CASE
	WHEN avg_price < 50 THEN 'Budget Seller'
    WHEN avg_price >= 50 and avg_price <= 150 THEN 'Standard Seller'
    ELSE 'Premium Seller'
END AS price_category
FROM slrs;


WITH customer_spending AS
(SELECT c.customer_unique_id, SUM(op.payment_value) as total_spending
FROM order_payments  AS op
INNER JOIN orders AS o 
ON o.order_id = op.order_id
INNER JOIN customers AS c
ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id)

SELECT * FROM customer_spending
WHERE 
total_spending > (SELECT AVG(total_spending) FROM customer_spending)

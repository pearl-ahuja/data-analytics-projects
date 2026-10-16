SELECT 
	p.product_category_name , SUM(oi.price) AS revenue
FROM 
	products AS p
INNER JOIN
	order_items AS oi
ON
	oi.product_id = p.product_id
GROUP BY
	p.product_category_name
ORDER BY
	revenue DESC
LIMIT 1;


SELECT 
	c.customer_unique_id , SUM(op.payment_value) AS spending
FROM 
	customers AS c
INNER JOIN
	orders AS o
ON
	o.customer_id = c.customer_id
INNER JOIN
	order_payments AS op
ON
	op.order_id = o.order_id
GROUP BY
	c.customer_unique_id
ORDER BY
	spending DESC
LIMIT 10;



SELECT 
	seller_id, COUNT( DISTINCT product_id) AS unique_products
FROM
	order_items
GROUP BY
	seller_id
ORDER BY
	unique_products DESC;
    
    
    
SELECT c.customer_state, COUNT(DISTINCT o.order_id) AS total_orders
FROM 
	customers AS c
INNER JOIN
	orders AS o
ON 
	c.customer_id = o.customer_id
GROUP BY
	c.customer_state
ORDER BY
	total_orders DESC;

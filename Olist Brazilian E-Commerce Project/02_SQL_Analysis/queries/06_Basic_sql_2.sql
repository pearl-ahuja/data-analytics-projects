SELECT COUNT(DISTINCT customer_unique_id)
FROM customers;

SELECT COUNT(DISTINCT customer_city)
FROM customers;


SELECT 
	customer_city,
	COUNT(*) AS customers
FROM
	customers 
GROUP BY 
	customer_city
ORDER BY 
	customers DESC;


SELECT
	order_status,
    COUNT(*) AS count
FROM
	orders
GROUP BY 
	order_status;
 
 
SELECT
	order_status,
    COUNT(*) AS count
FROM
	orders
GROUP BY 
	order_status
HAVING 
	order_status = 'delivered';
    
    
SELECT payment_type, AVG(payment_value)
FROM order_payments
GROUP BY payment_type;


SELECT MAX(freight_value) FROM order_items;

SELECT MIN(product_weight_g) FROM products;
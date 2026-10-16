SELECT 
	MONTHNAME(o.order_purchase_timestamp)
		AS month_name,
	SUM(oi.price)
		AS monthly_revenue,
	LAG(SUM(oi.price)) OVER(
        ORDER BY MONTH(o.order_purchase_timestamp)
) 
        AS prev_month_revenue
FROM
	orders AS o
INNER JOIN
	order_items AS oi
ON
	o.order_id = oi.order_id
GROUP BY 	
	month_name,
    MONTH(o.order_purchase_timestamp);




WITH delivery_info AS(
SELECT 
	c.customer_state, 
    DATEDIFF (o.order_delivered_customer_date,
    o.order_purchase_timestamp) AS delivery_days
FROM
	orders AS o
INNER JOIN
	customers AS c
ON c.customer_id= o.customer_id)
SELECT 
	customer_state,
    AVG(delivery_days) AS avg_delivery_time
FROM 
	delivery_info
GROUP BY 
	customer_state;
    
    
    

SELECT
	DATE_FORMAT(o.order_purchase_timestamp,'%Y-%m') AS Month_Year,
    SUM(oi.price) AS revenue
FROM orders AS o
INNER JOIN order_items AS oi
ON o.order_id = oi.order_id
GROUP BY DATE_FORMAT(o.order_purchase_timestamp,'%Y-%m');



SELECT product_id, COALESCE(product_weight_g,0)
FROM products;

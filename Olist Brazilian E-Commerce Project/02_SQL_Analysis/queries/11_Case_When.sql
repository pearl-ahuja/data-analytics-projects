SELECT review_score, 
CASE 
	WHEN review_score <= 2 THEN 'POOR'
    WHEN review_score = 3 THEN 'AVERAGE'
    ELSE 'EXCELLENT'
END AS review_category
FROM order_reviews;

SELECT order_id, price,  
CASE 
	WHEN price < 50 THEN 'CHEAP'
    WHEN price >= 50 and price <= 200 THEN 'MODERATE'
    ELSE 'EXPENSIVE'
END AS price_category
FROM order_items;



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



SELECT order_id,
CASE
	WHEN order_delivered_customer_date < order_estimated_delivery_date THEN 'On Time'
    ELSE 'Late'
END AS delivery_category
FROM orders;



WITH rev_category AS
(SELECT  
CASE 
	WHEN review_score <= 2 THEN 'POOR'
    WHEN review_score = 3 THEN 'AVERAGE'
    ELSE 'EXCELLENT'
END AS review_category
FROM order_reviews)

SELECT review_category,COUNT(review_category)
FROM rev_category
GROUP BY review_category;
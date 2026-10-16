USE olist_ecommerce;

SELECT *
FROM customers;

SELECT customer_id, customer_city, customer_state
FROM customers;

SELECT *
FROM customers
LIMIT 10;


SELECT *
FROM customers
ORDER BY 
customer_state,
customer_city DESC;


SELECT DISTINCT 
customer_state 
FROM customers;


SELECT *
FROM customers 
WHERE 
customer_state IN ('SP', 'RJ', 'MG');

SELECT *
FROM customers 
WHERE 
customer_state NOT IN ('SP', 'RJ', 'MG');


SELECT *
FROM customers 
WHERE 
customer_city LIKE 'sao%' ;
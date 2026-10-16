SELECT product_id, product_category_name
FROM products
WHERE product_category_name = 'health_beauty'
UNION
SELECT product_id, product_category_name
FROM products
WHERE product_category_name = 'sports_leisure';

SELECT product_id, product_category_name
FROM products
WHERE product_category_name IN ('sport_leisure','health_beauty');




# INDEXING IS DONE  TO THE COLUMNS FREQUENTLY USED TO MAKE SEARCHING, SORTING, FILTERING FASTER
# BUT USING IT FOR EVERY OTHER COLUMN WILL TAKE UP SO MUCH STORAGE AND REDUCE EFFICIENCY 

# EXPLAIN HELP US UNDERSTAND HOW IS SQL EXECUTING EVERY QUERY 
WITH prod_cat as
(
SELECT p.product_category_name,p.product_id, sum(o.price) as total_price
FROM products as p
INNER JOIN
order_items as o
ON p.product_id = o.product_id
GROUP BY p.product_id,p.product_category_name
),
Row_num AS
(
SELECT product_id, product_category_name, total_price,
ROW_NUMBER() OVER(
PARTITION BY product_category_name
ORDER BY total_price DESC
) AS rn
FROM prod_cat)
SELECT * FROM Row_num
WHERE rn <=3;



WITH seller_info AS
(
SELECT s.seller_id, s.seller_state, sum(oi.price) as revenue
FROM sellers as s
INNER JOIN
order_items as oi
ON s.seller_id = oi.seller_id
GROUP BY s.seller_id, s.seller_state
),
ranked_sellers AS
(SELECT seller_id, seller_state, revenue,
ROW_NUMBER() OVER(
PARTITION BY seller_state
ORDER BY revenue DESC
) AS rn
FROM seller_info
)
SELECT * FROM ranked_sellers
WHERE rn<=3;
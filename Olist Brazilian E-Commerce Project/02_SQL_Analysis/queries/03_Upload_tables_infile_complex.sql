LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Products.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(
product_id,
product_category_name,
@product_name_length,
@product_description_length,
@product_photos_qty,
@product_weight_g,
@product_length_cm,
@product_height_cm,
@product_width_cm
)
SET
product_name_length = NULLIF(@product_name_length,''),
product_description_length = NULLIF(@product_description_length,''),
product_photos_qty = NULLIF(@product_photos_qty,''),
product_weight_g = NULLIF(@product_weight_g,''),
product_length_cm = NULLIF(@product_length_cm,''),
product_height_cm = NULLIF(@product_height_cm,''),
product_width_cm = NULLIF(@product_width_cm,'');
use olist_ecommerce;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Order_Reviews.csv'
INTO TABLE order_reviews
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(
review_id,
order_id,
review_score,
review_comment_title,
review_comment_message,
@review_creation_date,
@review_answer_timestamp
)
SET
review_creation_date =
    STR_TO_DATE(NULLIF(@review_creation_date,''), '%d-%m-%Y %H:%i'),

review_answer_timestamp =
    STR_TO_DATE(NULLIF(@review_answer_timestamp,''), '%d-%m-%Y %H:%i');
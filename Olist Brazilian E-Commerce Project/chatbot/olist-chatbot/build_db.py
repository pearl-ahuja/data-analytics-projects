"""Builds olist.duckdb from the cleaned CSVs. Run once: python build_db.py <folder_with_csvs>"""
import sys, os, duckdb

src = sys.argv[1] if len(sys.argv) > 1 else "csv"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "olist.duckdb")
if os.path.exists(out):
    os.remove(out)
con = duckdb.connect(out)

def csv(name):
    return f"read_csv_auto('{os.path.join(src, name)}.csv', header=true, all_varchar=true)"

def ts(col):  # dates in the cleaned files are dd-mm-yyyy HH:MM
    return f"try_strptime(NULLIF(TRIM({col}),''), '%d-%m-%Y %H:%M') AS {col}"

con.execute(f"""CREATE TABLE customers AS SELECT customer_id, customer_unique_id,
  customer_zip_code_prefix::INT AS customer_zip_code_prefix, customer_city, customer_state FROM {csv('customers')}""")

con.execute(f"""CREATE TABLE sellers AS SELECT seller_id, seller_zip_code_prefix::INT AS seller_zip_code_prefix,
  seller_city, seller_state FROM {csv('sellers')}""")

con.execute(f"""CREATE TABLE product_category_translation AS SELECT * FROM {csv('product_category_translation')}""")

con.execute(f"""CREATE TABLE products AS SELECT product_id, product_category_name,
  TRY_CAST(product_name_lenght AS INT) AS product_name_length,
  TRY_CAST(product_description_lenght AS INT) AS product_description_length,
  TRY_CAST(product_photos_qty AS INT) AS product_photos_qty,
  TRY_CAST(product_weight_g AS INT) AS product_weight_g,
  TRY_CAST(product_length_cm AS INT) AS product_length_cm,
  TRY_CAST(product_height_cm AS INT) AS product_height_cm,
  TRY_CAST(product_width_cm AS INT) AS product_width_cm FROM {csv('products')}""")

con.execute(f"""CREATE TABLE orders AS SELECT order_id, customer_id, TRIM(order_status) AS order_status,
  {ts('order_purchase_timestamp')}, {ts('order_approved_at')}, {ts('order_delivered_carrier_date')},
  {ts('order_delivered_customer_date')}, {ts('order_estimated_delivery_date')} FROM {csv('orders')}""")

con.execute(f"""CREATE TABLE order_items AS SELECT order_id, order_item_id::INT AS order_item_id, product_id, seller_id,
  {ts('shipping_limit_date')}, price::DECIMAL(10,2) AS price, freight_value::DECIMAL(10,2) AS freight_value
  FROM {csv('order_items')}""")

con.execute(f"""CREATE TABLE order_payments AS SELECT order_id, payment_sequential::INT AS payment_sequential,
  payment_type, payment_installments::INT AS payment_installments, payment_value::DECIMAL(10,2) AS payment_value
  FROM {csv('order_payments')}""")

con.execute(f"""CREATE TABLE order_reviews AS SELECT review_id, order_id, review_score::INT AS review_score,
  review_comment_title, review_comment_message, {ts('review_creation_date')}, {ts('review_answer_timestamp')}
  FROM {csv('order_reviews')}""")

# Friendly view: products with English category names
con.execute("""CREATE VIEW products_en AS
  SELECT p.*, COALESCE(t.product_category_name_english, p.product_category_name) AS category_english
  FROM products p LEFT JOIN product_category_translation t USING (product_category_name)""")

for t in ["customers","sellers","products","orders","order_items","order_payments","order_reviews"]:
    print(t, con.execute(f"select count(*) from {t}").fetchone()[0])
con.close()
print("size MB:", round(os.path.getsize(out)/1e6,1))

"""Core logic: safe SQL execution + question -> SQL -> answer pipeline."""
import json, os, re
import duckdb
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data", "olist.duckdb")
MAX_ROWS = 200

SCHEMA = """
Database engine: DuckDB (SQL dialect similar to PostgreSQL). Read-only.

TABLES
customers(customer_id PK, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
sellers(seller_id PK, seller_zip_code_prefix, seller_city, seller_state)
products(product_id PK, product_category_name [Portuguese], product_name_length, product_description_length, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm)
product_category_translation(product_category_name, product_category_name_english)
products_en  -- VIEW = products + category_english (English name). ALWAYS use this for category questions.
orders(order_id PK, customer_id FK, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date)  -- all TIMESTAMP
order_items(order_id FK, order_item_id, product_id FK, seller_id FK, shipping_limit_date, price, freight_value)  -- PK (order_id, order_item_id); one row per item
order_payments(order_id FK, payment_sequential, payment_type, payment_installments, payment_value)  -- an order can have several payment rows
order_reviews(review_id, order_id FK, review_score 1-5, review_comment_title, review_comment_message [Portuguese], review_creation_date, review_answer_timestamp)

JOINS: orders.customer_id = customers.customer_id ; order_items.order_id = orders.order_id ;
order_items.product_id = products_en.product_id ; order_items.seller_id = sellers.seller_id ;
order_payments.order_id = orders.order_id ; order_reviews.order_id = orders.order_id.

DATA NOTES
- order_status values: delivered, shipped, canceled, unavailable, invoiced, processing, created, approved.
- Data covers 2016-09 to 2018-10. State columns are 2-letter Brazilian codes (SP, RJ, MG...). City names are lowercase without accents.
- Delivery timestamps are NULL for orders not delivered. Filter them out for delivery-time maths.
- Beware fan-out: joining order_items / order_payments / order_reviews together multiplies rows. Aggregate each table separately (CTE/subquery) before joining, or use COUNT(DISTINCT order_id).
- Use DuckDB functions: date_trunc('month', ts), date_diff('day', a, b), strftime(ts, '%Y-%m'), year(ts), month(ts).

METRIC DEFINITIONS (match the Power BI dashboard)
- Revenue = SUM(order_items.price) (freight excluded). Orders = COUNT(DISTINCT order_id). AOV = revenue / orders.
- Customers = COUNT(DISTINCT customer_unique_id). Bad review = review_score <= 2.
- Late delivery = order_delivered_customer_date > order_estimated_delivery_date.
- Delivery time (days) = date_diff('day', order_purchase_timestamp, order_delivered_customer_date).
"""

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|attach|detach|copy|pragma|install|load|export|import|call|"
    r"execute|set|read_csv|read_csv_auto|read_parquet|read_json|read_text|glob|checkpoint|vacuum|truncate|"
    r"replace\s+into|from_csv|parquet_scan|sniff_csv)\b", re.I)


class UnsafeSQL(Exception):
    pass


def validate_sql(sql: str) -> str:
    s = (sql or "").strip().rstrip(";").strip()
    if not s:
        raise UnsafeSQL("Empty query.")
    if ";" in re.sub(r"'[^']*'", "", s):
        raise UnsafeSQL("Only a single statement is allowed.")
    if not re.match(r"^(select|with)\b", s, re.I):
        raise UnsafeSQL("Only SELECT queries are allowed.")
    if FORBIDDEN.search(re.sub(r"'[^']*'", "''", s)):
        raise UnsafeSQL("Query contains a blocked keyword.")
    return s


def get_connection():
    con = duckdb.connect(DB_PATH, read_only=True)
    con.execute("SET memory_limit='700MB'")
    con.execute("SET threads=2")
    con.execute("SET enable_external_access=false")
    con.execute("SET lock_configuration=true")
    return con


def run_sql(con, sql: str) -> pd.DataFrame:
    safe = validate_sql(sql)
    df = con.execute(f"SELECT * FROM ({safe}) AS q LIMIT {MAX_ROWS}").fetchdf()
    for col in df.columns:  # Decimal -> float so charts/tables render cleanly
        if df[col].dtype == object and len(df) and df[col].map(lambda v: v.__class__.__name__ == "Decimal").all():
            df[col] = df[col].astype(float)
    return df


def load_context() -> str:
    with open(os.path.join(BASE, "project_context.md"), encoding="utf-8") as f:
        return f.read()


PLAN_PROMPT = """You are the data assistant embedded in a recruiter-facing portfolio project: an Olist Brazilian
E-Commerce analysis (Excel/Power Query -> MySQL -> Power BI). Visitors ask questions about the project and its data.

{schema}

PROJECT CONTEXT
{context}

{history}
Decide how to answer the visitor's latest question and reply with ONLY a JSON object:
{{"mode": "sql" | "context" | "off_topic",
  "sql": "<one DuckDB SELECT query, only if mode is sql>",
  "answer": "<short answer, only if mode is context or off_topic>"}}

Rules:
- mode "sql": the question needs numbers/rankings/trends from the data. Write ONE read-only SELECT (or WITH ... SELECT).
  Give columns readable aliases, round decimals to 2, ORDER meaningfully, and add LIMIT 20 unless asked for more.
  Use products_en.category_english for categories. Follow the metric definitions exactly.
- mode "context": the question is about the project itself (tools used, workflow, cleaning steps, dashboard pages,
  skills, design choices) and the PROJECT CONTEXT answers it. Answer in first person as the project's author, briefly.
  If the context does not contain the answer, say that honestly instead of inventing details.
- mode "off_topic": unrelated to this project/data. Politely steer back with 2-3 example questions.
- Never invent data. Never write anything except the JSON object.

Visitor's question: {question}
"""

FIX_PROMPT = """Your previous query failed.
Question: {question}
SQL: {sql}
Error: {error}
Return ONLY a JSON object {{"mode":"sql","sql":"<corrected DuckDB SELECT>"}}.
Schema reminder:
{schema}
"""

ANSWER_PROMPT = """You are the data assistant for a portfolio project (Olist Brazilian E-Commerce analysis).
A visitor asked: {question}
This SQL was run on the data:
{sql}
Result ({n} rows{trunc}):
{table}

Write a clear answer for a recruiter-level reader in 2-5 sentences. Lead with the direct answer, cite the key numbers
from the result only (never invent numbers), and add one short insight or caveat if useful (e.g. what a metric includes).
Currency is Brazilian Real (BRL). Plain text, light markdown allowed. If the result is empty, say no data matched."""


def _history_block(history):
    if not history:
        return ""
    lines = ["RECENT CONVERSATION (for follow-up questions):"]
    for h in history[-3:]:
        lines.append(f"Q: {h['q']}")
        if h.get("sql"):
            lines.append(f"SQL used: {h['sql']}")
    return "\n".join(lines) + "\n"


def _parse_json(text: str) -> dict:
    t = (text or "").strip()
    t = re.sub(r"^```(?:json)?|```$", "", t, flags=re.M).strip()
    m = re.search(r"\{.*\}", t, re.S)
    return json.loads(m.group(0) if m else t)


def answer_question(question: str, con, llm, history=None):
    """llm: callable(prompt:str, json_mode:bool)->str. Returns dict(answer, sql, df, mode)."""
    context = load_context()
    plan = _parse_json(llm(PLAN_PROMPT.format(schema=SCHEMA, context=context,
                                              history=_history_block(history), question=question), True))
    mode = plan.get("mode")
    if mode in ("context", "off_topic"):
        return {"mode": mode, "answer": plan.get("answer", "").strip(), "sql": None, "df": None}

    sql, df, err = plan.get("sql", ""), None, None
    for attempt in range(2):
        try:
            df = run_sql(con, sql)
            err = None
            break
        except UnsafeSQL as e:
            return {"mode": "blocked", "answer": f"I can only run read-only SELECT queries on this dataset ({e})",
                    "sql": sql, "df": None}
        except Exception as e:  # SQL error -> one self-repair attempt
            err = str(e)
            if attempt == 0:
                fixed = _parse_json(llm(FIX_PROMPT.format(question=question, sql=sql, error=err, schema=SCHEMA), True))
                sql = fixed.get("sql", sql)
    if df is None:
        return {"mode": "error", "answer": "I couldn't turn that into a working query. Try rephrasing it a little, "
                "for example by naming the table or metric you care about.", "sql": sql, "df": None}

    shown = df.head(30)
    text = llm(ANSWER_PROMPT.format(question=question, sql=sql, n=len(df),
                                    trunc=" (showing first 30)" if len(df) > 30 else "",
                                    table=shown.to_csv(index=False)), False)
    return {"mode": "sql", "answer": text.strip(), "sql": sql, "df": df}

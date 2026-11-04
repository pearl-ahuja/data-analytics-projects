import os, re, datetime
import pandas as pd
import streamlit as st
from engine import get_connection, answer_question

# ---------- EDIT THESE ----------
OWNER_NAME = "Pearl Ahuja"
GITHUB_URL = "https://github.com/pearl-ahuja/data-analytics-projects/tree/main/Olist%20Brazilian%20E-Commerce%20Project"
LINKEDIN_URL = ""   # optional, e.g. "https://www.linkedin.com/in/your-id"
SESSION_LIMIT = 15      # questions per visitor session
DAILY_LIMIT = 250       # total questions per day across all visitors (protects the free quota)
# --------------------------------

st.set_page_config(page_title="Olist Project Chatbot", page_icon="💬", layout="wide")

STARTERS = [
    "Which 5 product categories earn the most revenue?",
    "How did monthly revenue change from 2017 to 2018?",
    "Which states have the slowest average delivery time?",
    "Do late deliveries get worse review scores?",
    "What did you do to clean the data?",
    "Which payment types are most popular?",
]


@st.cache_resource
def db():
    return get_connection()


@st.cache_resource
def counters():
    return {"day": None, "n": 0, "cache": {}}


def secret(name, default=""):
    try:
        return st.secrets[name]
    except Exception:  # no secrets file, or key missing -> fall back to environment variable
        return os.environ.get(name, default)


@st.cache_resource
def get_llm():
    from llm import make_llm
    key = secret("GEMINI_API_KEY")
    if not key:
        return None
    return make_llm(key, secret("GEMINI_MODELS", "gemini-2.5-flash-lite,gemini-2.5-flash"))


def daily_ok():
    c, today = counters(), datetime.date.today()
    if c["day"] != today:
        c["day"], c["n"] = today, 0
    return c["n"] < DAILY_LIMIT


@st.cache_data(ttl=3600)
def kpis():
    q = lambda s: db().execute(s).fetchone()[0]
    rev = float(q("select sum(price) from order_items"))
    orders = q("select count(*) from orders")
    return {"Revenue (BRL)": f"{rev/1e6:.2f}M", "Orders": f"{orders/1e3:.0f}K",
            "AOV (BRL)": f"{rev/orders:.2f}",
            "Avg review": f"{float(q('select avg(review_score) from order_reviews')):.2f}"}


def show_df(df: pd.DataFrame):
    st.dataframe(df, width='stretch', hide_index=True)
    if df.shape[1] == 2 and pd.api.types.is_numeric_dtype(df.iloc[:, 1]) and 2 <= len(df) <= 40:
        chart = df.set_index(df.columns[0])
        label = df.columns[0].lower()
        (st.line_chart if re.search(r"month|date|year|day|week", label) else st.bar_chart)(chart)


# ---------- sidebar ----------
with st.sidebar:
    st.header("About this project")
    st.write("End-to-end analysis of the **Olist Brazilian E-Commerce** dataset: "
             "Excel / Power Query cleaning → MySQL analysis → Power BI dashboard.")
    cols = st.columns(2)
    for (k, v), col in zip(kpis().items(), cols * 2):
        col.metric(k, v)
    st.caption("Live from the same cleaned data the dashboard uses.")
    st.markdown(f"[GitHub repository]({GITHUB_URL})" + (f" · [LinkedIn]({LINKEDIN_URL})" if LINKEDIN_URL else ""))
    st.divider()
    st.subheader("Try asking")
    for s in STARTERS:
        if st.button(s, width='stretch', key=s):
            st.session_state["pending"] = s
    st.divider()
    st.caption("How it works: your question → AI writes a read-only SQL query → it runs on the project data → "
               "the answer is explained in plain English. Open **Show SQL** under any answer to verify it.")

# ---------- main ----------
st.title("💬 Ask my Olist project anything")
st.write(f"Built by **{OWNER_NAME}**. Ask about revenue, delivery, reviews, sellers, or how I built the project. "
         "No dashboard filters needed — just ask.")

if "messages" not in st.session_state:
    st.session_state.messages, st.session_state.history, st.session_state.used = [], [], 0

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("df") is not None:
            show_df(m["df"])
        if m.get("sql"):
            with st.expander("Show SQL"):
                st.code(m["sql"], language="sql")

typed = st.chat_input("e.g. Which state has the highest average order value?")
question = st.session_state.pop("pending", None) or typed

if question:
    question = question.strip()[:400]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        llm = get_llm()
        if llm is None:
            res = {"answer": "The chatbot isn't configured yet (missing API key).", "sql": None, "df": None}
        elif st.session_state.used >= SESSION_LIMIT:
            res = {"answer": "You've reached the question limit for this session. Thanks for exploring! "
                   "Refresh the page to start again, or see the GitHub repo for the full analysis.",
                   "sql": None, "df": None}
        elif not daily_ok():
            res = {"answer": "The demo has hit its daily free-tier limit. Please try again tomorrow, "
                   "or explore the Power BI screenshots and SQL in the GitHub repo.", "sql": None, "df": None}
        else:
            c, key = counters(), question.lower()
            first_turn = not st.session_state.history
            if first_turn and key in c["cache"]:
                res = c["cache"][key]
            else:
                with st.spinner("Writing the query and crunching the data…"):
                    try:
                        res = answer_question(question, db(), llm, st.session_state.history)
                        c["n"] += 1
                        st.session_state.used += 1
                        if first_turn and res.get("mode") in ("sql", "context"):
                            c["cache"][key] = res
                    except Exception as e:
                        msg = str(e)
                        busy = "RateLimited" in type(e).__name__ or "429" in msg or "RESOURCE_EXHAUSTED" in msg
                        res = {"answer": ("I'm getting a lot of questions right now (free-tier limit). "
                                          "Please try again in a minute." if busy else
                                          "Something went wrong on my side. Please try rephrasing the question."),
                               "sql": None, "df": None}
        st.markdown(res["answer"])
        if res.get("df") is not None:
            show_df(res["df"])
        if res.get("sql"):
            with st.expander("Show SQL"):
                st.code(res["sql"], language="sql")
    st.session_state.messages.append({"role": "assistant", "content": res["answer"],
                                      "df": res.get("df"), "sql": res.get("sql")})
    st.session_state.history.append({"q": question, "sql": res.get("sql")})

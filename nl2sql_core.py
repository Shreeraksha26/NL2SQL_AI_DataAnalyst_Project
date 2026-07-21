"""
nl2sql_core.py
--------------
Shared logic used by both cli.py and app.py:
1. get_schema()        -> reads the actual table structure from sample_data.db
2. question_to_sql()   -> asks Gemini to turn a plain-English question into SQL
3. run_sql()           -> safely executes that SQL (read-only) and returns rows
4. summarize_results() -> asks Gemini to explain the result in plain English

Uses Google's Gemini API, which has a genuinely free tier (no credit card
required). Get a free key at https://aistudio.google.com/apikey

Requires the key set as an environment variable:
    export GEMINI_API_KEY="your-key-here"      (Mac/Linux)
    $env:GEMINI_API_KEY="your-key-here"         (Windows PowerShell)
"""

import os
import sqlite3
import re
import pandas as pd
from google import genai

DB_NAME = "sample_data.db"
MODEL = "gemini-2.5-flash"  # fast, capable, and on Google's free tier


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Get a free key at https://aistudio.google.com/apikey "
            "and set it as an environment variable before running this."
        )
    return genai.Client(api_key=api_key)


def get_schema(db_path: str = DB_NAME) -> str:
    """Reads the actual CREATE TABLE statements from the SQLite file,
    so the prompt we send Gemini always matches the real database."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL")
    rows = cur.fetchall()
    conn.close()
    return "\n\n".join(row[0] for row in rows)


def question_to_sql(question: str, schema: str) -> str:
    """Sends the schema + question to Gemini and asks for ONE SQL query back."""
    client = get_client()

    prompt = (
        "You are a SQL assistant for a SQLite database. Given a database schema and a "
        "plain-English question, respond with ONLY a single valid SQLite SELECT query "
        "that answers the question. Rules:\n"
        "- Only ever generate SELECT statements. Never INSERT, UPDATE, DELETE, DROP, or ALTER.\n"
        "- Do not include any explanation, markdown formatting, or code fences.\n"
        "- Return the raw SQL only.\n\n"
        f"Database schema:\n{schema}\n\n"
        f"Question: {question}"
    )

    response = client.models.generate_content(model=MODEL, contents=prompt)
    sql = response.text.strip()
    # Strip markdown code fences if the model adds them anyway
    sql = re.sub(r"^```sql\s*|^```\s*|```$", "", sql, flags=re.MULTILINE).strip()
    return sql


def is_safe_select(sql: str) -> bool:
    """Basic guardrail: only allow single SELECT statements.
    This is a demo project safeguard, not a production-grade SQL sanitizer."""
    normalized = sql.strip().lower()
    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "attach", ";--"]
    if not normalized.startswith("select"):
        return False
    if any(word in normalized for word in forbidden):
        return False
    if sql.count(";") > 1:
        return False
    return True


def run_sql(sql: str, db_path: str = DB_NAME) -> pd.DataFrame:
    if not is_safe_select(sql):
        raise ValueError(
            f"Refusing to run this query for safety reasons (only single SELECT statements "
            f"are allowed in this demo):\n{sql}"
        )
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def summarize_results(question: str, df: pd.DataFrame) -> str:
    """Asks Gemini to explain the query result in a short, plain-English sentence or two."""
    client = get_client()

    # Keep the sample small so we don't send huge result sets to the API
    sample = df.head(20).to_csv(index=False)

    prompt = (
        f"The user asked: \"{question}\"\n\n"
        f"Here is the resulting data (CSV, showing up to 20 rows):\n{sample}\n\n"
        "In 1-3 plain English sentences, summarize the key insight from this data for "
        "someone who doesn't want to read the raw table. Be specific with numbers where relevant."
    )

    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text.strip()

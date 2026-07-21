# AI-Powered Natural Language → SQL Data Analyst (Demo Project)

Ask a question in plain English (e.g. *"Which product generated the most revenue?"*),
and this project:
1. Converts your question into a real SQL query using Google's Gemini API,
2. Runs that query against a sample e-commerce SQLite database,
3. Summarizes the result back to you in plain English.

This uses Google Gemini specifically because it has a genuinely free tier — no credit
card required to get started.

This is a genuinely runnable, working project — not just a mockup — so you can actually
demo it, screen-record it, and speak to how it works in an interview.

---

## 1. Setup (one-time)

**Step 1 — Install Python packages**
```bash
pip install -r requirements.txt
```

**Step 2 — Create the sample database**
```bash
python setup_database.py
```
This creates `sample_data.db` — a small e-commerce database with customers, products,
orders, and order_items (120 sample orders).

**Step 3 — Get a free Google Gemini API key**
- Go to https://aistudio.google.com/apikey, sign in with a Google account, and click
  "Create API key". No credit card required.
- Set it as an environment variable:

```bash
# Mac/Linux
export GEMINI_API_KEY="your-key-here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your-key-here

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-key-here"
```

---

## 2. Running it

**Option A — Terminal version (simplest, good for quick testing)**
```bash
python cli.py
```
Then type questions like:
- `Which product generated the most revenue?`
- `How many orders came from customers in Bengaluru?`
- `What is the average order value?`

**Option B — Web UI version (better for a demo/screen recording)**
```bash
streamlit run app.py
```
This opens a browser tab with a text box, the generated SQL, a results table, and a
plain-English summary — this is the version worth recording a 30-60 second demo of.

---

## 3. How it works (for your interview prep)

- `setup_database.py` — builds a small sample SQLite database so there's real data to query.
- `nl2sql_core.py` — the core logic:
  - `get_schema()` reads the actual table structure from the database, so the AI always
    knows the real column names (instead of you hardcoding them).
  - `question_to_sql()` sends your question + the schema to Gemini and asks for one SQL
    query back.
  - `is_safe_select()` is a guardrail that only allows single `SELECT` statements —
    it blocks `DELETE`, `DROP`, `UPDATE`, etc., so the AI can never modify or destroy data.
  - `run_sql()` actually executes the query and returns a pandas DataFrame.
  - `summarize_results()` sends the result back to Gemini and asks for a short,
    plain-English explanation.
- `cli.py` / `app.py` — two different front-ends (terminal vs. browser) for the same
  core logic.

## 4. Extending it further (optional, if you want to go deeper)

- Swap the sample SQLite database for a real dataset (e.g., a Kaggle e-commerce dataset).
- Add a chat history so follow-up questions ("now break that down by city") work.
- Add basic query result caching to avoid repeat API calls for the same question.
- Deploy the Streamlit app publicly (Streamlit Community Cloud is free) so you can share
  a live link instead of just a screen recording.

## 5. Resume bullet you can honestly use once you've run this

> Built an AI-powered natural language-to-SQL assistant using Python and Google's Gemini
> API, enabling plain-English querying of a relational database with automatic SQL
> generation, safe query execution, and AI-generated insight summaries.

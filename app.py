"""
app.py
------
Streamlit UI for the AI-powered Natural Language -> SQL Assistant.
Good for a visual demo (e.g., a screen recording to show recruiters).

Setup:
    1. pip install -r requirements.txt
    2. python setup_database.py          (only needed once)
    3. export GEMINI_API_KEY="your-key-here"   (get a free key at aistudio.google.com/apikey)
    4. streamlit run app.py
"""

import streamlit as st
import nl2sql_core as core

st.set_page_config(page_title="AI Data Analyst", page_icon="\U0001F4CA", layout="centered")

st.title("\U0001F4CA AI-Powered Data Analyst")
st.caption("Ask a question in plain English. Get SQL, real data, and a plain-English insight.")

with st.expander("Example questions to try"):
    st.markdown(
        "- Which product generated the most revenue?\n"
        "- How many orders did we get from customers in Bengaluru?\n"
        "- What are the top 3 cities by number of orders?\n"
        "- What is the average order value?"
    )

question = st.text_input("Your question:", placeholder="e.g., Which product generated the most revenue?")

if st.button("Ask", type="primary") and question:
    try:
        schema = core.get_schema()

        with st.spinner("Generating SQL..."):
            sql = core.question_to_sql(question, schema)
        st.subheader("Generated SQL")
        st.code(sql, language="sql")

        with st.spinner("Running query..."):
            df = core.run_sql(sql)
        st.subheader(f"Results ({len(df)} rows)")
        st.dataframe(df, use_container_width=True)

        if not df.empty:
            with st.spinner("Summarizing..."):
                summary = core.summarize_results(question, df)
            st.subheader("Plain-English Insight")
            st.success(summary)
        else:
            st.info("The query ran successfully but returned no rows.")

    except Exception as e:
        st.error(str(e))

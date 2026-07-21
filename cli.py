"""
cli.py
------
Simplest way to run the project: a terminal loop.
Ask a question in plain English, get SQL + results + a summary.

Setup:
    1. pip install -r requirements.txt
    2. python setup_database.py          (only needed once)
    3. export GEMINI_API_KEY="your-key-here"   (get a free key at aistudio.google.com/apikey)
    4. python cli.py
"""

import nl2sql_core as core


def main():
    print("=" * 60)
    print("AI-Powered Natural Language -> SQL Assistant (demo)")
    print("Ask questions about the sample e-commerce database.")
    print("Type 'exit' to quit.")
    print("=" * 60)

    schema = core.get_schema()

    while True:
        question = input("\nYour question: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue

        try:
            sql = core.question_to_sql(question, schema)
            print(f"\nGenerated SQL:\n{sql}")

            df = core.run_sql(sql)
            print(f"\nResults ({len(df)} rows):")
            print(df.to_string(index=False) if not df.empty else "(no rows returned)")

            if not df.empty:
                summary = core.summarize_results(question, df)
                print(f"\nSummary: {summary}")

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()

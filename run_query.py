# run_query.py
import sqlite3, pandas as pd

conn = sqlite3.connect("ecom.db")
sql = open("query_example.sql").read()
df = pd.read_sql_query(sql, conn)
df.to_csv("query_output.csv", index=False)
print("Wrote query_output.csv with", len(df), "rows")
conn.close()

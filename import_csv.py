import sqlite3
import pandas as pd

# connect to SQLite
conn = sqlite3.connect("data_university.sqlite")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS universities (
        university TEXT,
        country TEXT,
        city TEXT,
        global_rank INTEGER
    )
""")

# CSV in Pandas
df = pd.read_csv('top_universities.csv')

df.to_sql("universities", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

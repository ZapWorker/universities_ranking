import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("data_university.sqlite")
cursor = conn.cursor()

output_folder = "my_results"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_path = os.path.join(output_folder, "university_analysis.xlsx")

# sql
queries = {
    "count_per_country": """
        SELECT country, COUNT(*) AS total_universities
        FROM universities
        GROUP BY country
        ORDER BY total_universities DESC;
    """,
    "best_in_czechia": """
        SELECT country, university, global_rank
        FROM universities
        WHERE country = "Czechia"
        ORDER BY global_rank ASC;
    """,
    "cities_with_50+": """
        SELECT city, COUNT(*) as total_city
        FROM universities
        GROUP BY city
        HAVING total_city > 50
        ORDER BY total_city DESC
    """,
    "best_in_country_rank<1000": """
    SELECT country, university, MIN(global_rank) AS best_rank
    FROM universities
    WHERE global_rank <= 1000
    GROUP BY country
    ORDER BY best_rank ASC;
    """,
    "distribution_per_country": """
        SELECT country,
            SUM(CASE WHEN global_rank <= 100 THEN 1 ELSE 0 END) AS top_100,
            SUM(CASE WHEN global_rank > 100 AND global_rank <= 500 THEN 1 ELSE 0 END) AS top_500,
            SUM(CASE WHEN global_rank > 500 THEN 1 ELSE 0 END) AS below_500
        FROM universities
        GROUP BY country
        ORDER BY top_100 DESC;
    """

}

# create excel
with pd.ExcelWriter(output_path) as writer:
    for sheet_name, query in queries.items():
        cursor.execute(query)
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])  
        df.to_excel(writer, sheet_name=sheet_name, index=False)

conn.close()

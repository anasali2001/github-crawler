import csv
from src.db.connection import get_connection

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM github.repositories")
        rows = cur.fetchall()

with open("repositories.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "owner", "name", "stars", "last_crawled_at"])
    writer.writerows(rows)

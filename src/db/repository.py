from src.db.connection import get_connection

def upsert_repository(repo_id, owner, name, stars, crawled_at):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO github.repositories
                (id, owner, name, stars, last_crawled_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id)
                DO UPDATE SET
                    stars = EXCLUDED.stars,
                    last_crawled_at = EXCLUDED.last_crawled_at
            """, (repo_id, owner, name, stars, crawled_at))

from datetime import datetime
from src.github_client import run_query
from src.db.repository import upsert_repository

QUERY = """
query ($cursor: String) {
  search(query: "stars:>0", type: REPOSITORY, first: 100, after: $cursor) {
    edges {
      node {
        ... on Repository {
          id
          name
          owner { login }
          stargazerCount
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""

def crawl(limit=100_000):
    cursor = None
    count = 0

    while count < limit:
        result = run_query(QUERY, {"cursor": cursor})
        search = result["data"]["search"]

        for edge in search["edges"]:
            repo = edge["node"]

            upsert_repository(
                repo_id=int(repo["id"], 16),
                owner=repo["owner"]["login"],
                name=repo["name"],
                stars=repo["stargazerCount"],
                crawled_at=datetime.utcnow(),
            )

            count += 1
            if count >= limit:
                break

        if not search["pageInfo"]["hasNextPage"]:
            break

        cursor = search["pageInfo"]["endCursor"]

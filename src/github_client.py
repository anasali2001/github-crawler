import requests
from tenacity import retry, wait_exponential, stop_after_attempt
from src.config import GITHUB_API_URL, GITHUB_TOKEN

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def run_query(query, variables=None):
    response = requests.post(
        GITHUB_API_URL,
        json={"query": query, "variables": variables},
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

import os

GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

CREATE SCHEMA IF NOT EXISTS github;

CREATE TABLE IF NOT EXISTS github.repositories (
    id TEXT PRIMARY KEY,
    owner TEXT NOT NULL,
    name TEXT NOT NULL,
    stars INTEGER NOT NULL,
    last_crawled_at TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_repos_stars
ON github.repositories(stars);

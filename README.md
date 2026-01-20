# GitHub Stars Crawler

## Overview
This project crawls GitHub repositories and stores their star counts using GitHub’s GraphQL API.  
The collected data is stored in a PostgreSQL database and exported as a CSV file using a GitHub Actions workflow.

The goal of this assignment is to demonstrate API usage, database design, CI/CD integration, and scalable data collection practices.

---

## Architecture
The project follows a simple layered structure:

- **GitHub Client**  
  Handles communication with GitHub’s GraphQL API, including pagination and retries.

- **Crawler**  
  Coordinates fetching repositories and persisting star data into the database.

- **Database Layer**  
  Responsible for schema creation, connections, and efficient inserts/updates.

- **CI Pipeline (GitHub Actions)**  
  Runs the crawler in a clean environment using a PostgreSQL service container and uploads results as an artifact.

---

## Database Schema
The database uses a dedicated schema (`github`) and stores repositories in a single table.

Each repository is identified using GitHub’s immutable GraphQL ID, which makes updates reliable and idempotent.

The schema is designed to:
- Support frequent updates without rewriting unnecessary rows
- Allow new metadata to be added without breaking existing data

---

## Schema Evolution and Future Metadata
To support additional GitHub data (issues, pull requests, comments, reviews, commits, CI checks), each entity would be stored in its own table.

Examples:
- `repositories`
- `issues`
- `pull_requests`
- `comments`
- `reviews`
- `commits`
- `ci_checks`

Each row would use GitHub’s ID as the primary key and reference its parent entity.  
When new data appears (e.g., new comments on a pull request), only new rows are inserted. Existing rows remain unchanged, minimizing database writes.

---

## Scaling Considerations
This implementation targets 100,000 repositories, where a single crawler and database are sufficient.

For much larger scales (hundreds of millions of repositories):
- Crawling would be distributed across multiple workers
- Repositories would be crawled incrementally instead of full re-crawls
- Crawl state would be tracked separately from repository data
- Database writes would be batched and sharded to avoid contention
- API usage would be carefully optimized to stay within rate limits

---

## CI/CD
The GitHub Actions pipeline:
1. Starts a PostgreSQL service container
2. Creates the database schema
3. Crawls repository star data using GitHub’s API
4. Dumps the database contents to a CSV file
5. Uploads the result as a workflow artifact

The pipeline uses the default GitHub Actions token and does not require any private secrets.

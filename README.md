## Scaling Considerations

This project is designed to crawl and store star counts for 100,000 GitHub repositories. At this scale, a single crawler, a single database, and daily re-crawls are sufficient.

If this system were extended to collect data for **500 million repositories**, the approach would need to change significantly:

* Crawling would be split across multiple independent workers, each responsible for a subset of repositories.
* Full re-crawls would be avoided. Instead, repositories would be re-crawled incrementally based on recent activity or last update time.
* Crawl state (last successful crawl, failures, retry timing) would be stored separately from repository metadata.
* Database writes would be batched, and unnecessary updates would be avoided to reduce write load.
* API usage would be tightly controlled by requesting only required fields and aggressively respecting GitHub rate limits.

These changes allow the system to scale without overwhelming the GitHub API or the database.

---

## Schema Evolution for Additional Metadata

The database schema is designed to evolve as more GitHub metadata is collected, such as issues, pull requests, comments, reviews, commits, and CI checks.

Instead of storing all data in a single table, each GitHub entity would have its own table:

* `repositories`
* `issues`
* `pull_requests`
* `comments`
* `reviews`
* `commits`
* `ci_checks`

Each row uses GitHub’s immutable GraphQL ID as the primary key. This makes updates simple and reliable.

For example, if a pull request has 10 comments today and 20 comments tomorrow:

* Only the 10 new comments are inserted as new rows.
* Existing comments are left untouched.
* The pull request row itself does not need to be updated.

This approach minimizes the number of rows affected during updates and keeps database operations efficient as data volume grows.

---

## Running the Crawler

The crawler is executed automatically via GitHub Actions. The workflow:

1. Starts a Postgres service container
2. Initializes the database schema
3. Crawls GitHub repository star data using the GitHub GraphQL API
4. Dumps the database contents into a CSV file
5. Uploads the result as a workflow artifact

---

# ✅ HOW TO MANUALLY RUN THE WORKFLOW

Right now your workflow runs on **push**:

```yaml
on: [push]
```

That means it only runs when you push code.

To manually run it, you need to add **workflow_dispatch**.

---

## Step 1: Update your workflow trigger

Edit `.github/workflows/crawl.yml` and change this:

```yaml
on: [push]
```

to this:

```yaml
on:
  push:
  workflow_dispatch:
```

This enables a **Run workflow** button in GitHub.

---

## Step 2: Commit and push

```powershell
git add .github/workflows/crawl.yml
git commit -m "Enable manual workflow trigger"
git push origin main
```

---

## Step 3: Manually run it in GitHub UI

1. Go to your GitHub repository
2. Click **Actions**
3. Click **GitHub Stars Crawler** (left sidebar)
4. Click **Run workflow**
5. Select the `main` branch
6. Click **Run workflow**

🎉 The pipeline will start immediately.

---

## Step 4: View results

* Click the running workflow
* Watch each step (Postgres → Crawl → Dump → Upload)
* Scroll down to **Artifacts**
* Download the CSV file

---


---
name: cosense-ingestion
description: Manages fetching and importing content from Cosense projects into the RAG system. Use when you need to sync new data or debug why data is missing from the search results.
---

# Cosense Ingestion Skill

This skill provides procedures for synchronizing data from Cosense using the `batch` service.

## Decision Tree: What is your goal?

1.  **I want to sync a specific project for the first time.**
    - Go to [Configure Ingestion](#1-configure-ingestion).
2.  **The latest changes in Cosense aren't appearing in search.**
    - Go to [Run Manual Ingestion](#2-run-manual-ingestion).
3.  **The ingestion process is failing or stuck.**
    - Go to [Troubleshooting Connection](#troubleshooting-connection).

## 1. Configure Ingestion

Before running ingestion, ensure the target project is configured:
- Target file: `batch/config.yaml` (or environment variables).
- Key parameter: `COSENSE_PROJECT_NAME`.

## 2. Run Manual Ingestion

To manually trigger an ingestion pass:
1.  Verify the `batch` container is running: `docker compose ps batch`
2.  Execute the ingestion script: `docker compose exec batch python main.py --sync`

## Troubleshooting Connection

- **Step 1**: Check if `scrapbox.io` is reachable: `curl -I https://scrapbox.io/api/pages/project-name`
- **Step 2**: Verify authentication tokens if the project is private (`connect.sid`).
- **Step 3**: Check `batch` service logs for rate-limiting errors (HTTP 429).

## Directories & Files

- `batch/`: Source code for the ingestion logic.
- `docs/DESIGN.md`: Detailed architecture of the Indexing Phase.

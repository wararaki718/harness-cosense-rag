---
name: project-setup-verification
description: Verifies the entire harness-cosense-rag stack is running correctly. Use at the start of any new session or when systemic failures occur.
---

# Project Setup Verification Skill

Use this skill to ensure the entire infrastructure is ready for development or testing.

## Decision Tree: What's the symptoms?

1.  **I just started working/cloned the repo.**
    - Action: Run [Full Stack Check](#full-stack-check).
2.  **I cannot connect to any service via the browser or cURL.**
    - Action: Run [Infrastructure Check](#1-infrastructure-check).
3.  **Local APIs are up, but data retrieval is empty.**
    - Action: Run [Dependency Connectivity Check](#2-dependency-connectivity-check).

## Full Stack Check

Check all services at once:
```bash
docker compose ps
```
All states should be "Up" or "Running".

## 1. Infrastructure Check

If containers are not running:
- Check for port conflicts (8000, 8001, 8080, 9200, 11434).
- Ensure Docker Desktop is active.
- Run: `docker compose up -d`

## 2. Dependency Connectivity Check

Verify if the backend can talk to the database and model:

- **Elasticsearch**: `curl http://localhost:9200`
- **SPLADE API**: `curl http://localhost:8001/health`
- **Ollama**: `curl http://localhost:11434`

## Checklist for readiness

- [ ] `docker compose ps` shows all 6 core components as healthy.
- [ ] `splade-api` health status is "ready".
- [ ] `elasticsearch` cluster status is "green" or "yellow".
- [ ] Environment variables (Cosense tokens, etc.) are loaded.

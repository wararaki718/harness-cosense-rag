---
name: splade-encoding
description: Instructions for converting text to sparse vectors using the splade-api. Use when indexing new documents or vectorizing user queries for retrieval.
---

# SPLADE Encoding Skill

This skill provides instructions for managing the text-to-vector conversion process via `splade-api`.

## Priority: Health Check

Before any encoding operation, ensure the model is loaded and ready. 
- **Command**: `curl http://localhost:8001/health`
- **Expected**: `{"status": "ready"}`
- If not ready, wait 30-60 seconds for the model to load into memory.

## Common Operations

### 1. Vectorize Query (Search Phase)
When a user asks a question, convert the question into a sparse vector.
- **Endpoint**: POST `/encode`
- **Payload**: `{"text": "User question here"}`

### 2. Batch Encoding (Indexing Phase)
When processing many documents from Cosense.
- See `scripts/batch_encode.py` for optimized processing.
- Run with `--help` for available options: `docker compose exec splade-api python scripts/batch_encode.py --help`

## Troubleshooting

- **Memory Errors**: Check Docker memory allocation (needs ~4GB for SPLADE).
- **Latency**: Ensure GPU support is correctly configured if response times exceed 1s.

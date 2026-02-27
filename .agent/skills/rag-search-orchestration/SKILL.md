---
name: rag-search-orchestration
description: Instructions for managing the search flow between search-api, elasticsearch, and llm-api. Use when debugging why a query returned a poor or incorrect answer.
---

# RAG Search Orchestration Skill

Management of the end-to-end RAG pipeline (Retrieval-Augmented Generation).

## Decision Tree: Debugging Poor Results

If the user says "the answer is wrong" or "no results found", use this tree:

1.  **Are there zero results from Elasticsearch?**
    - Yes: Go to [Retrieval Debugging](#1-retrieval-debugging).
    - No: Go to Step 2.
2.  **Does the LLM say "I don't know" despite relevant context being found?**
    - Yes: Go to [Prompt/LLM Debugging](#2-prompt-generation-debugging).
    - No: Go to Step 3.
3.  **Is the response slow or timing out?**
    - Yes: Go to [Performance Benchmarking](#3-performance-benchmarking).

## 1. Retrieval Debugging
- Check if the query vector is generated correctly (see `splade-encoding`).
- Verify indices in Elasticsearch: `GET /_cat/indices`
- Test raw ES retrieval with a known document ID.

## 2. Prompt & Generation Debugging
- Inspect the prompt sent to `llm-api`.
- Ensure the context length doesn't exceed LLM limits (Gemma3 context window).
- Verify `llm-api` is connected to Ollama: `curl http://localhost:11434/api/tags`

## 3. Performance Benchmarking
Check timing logs for:
- Encoding: ~100-300ms
- ES Search: ~50ms
- LLM Generation: ~2-5s (streaming)

## Directories & Files
- `search-api/`: Orchestration logic.
- `llm-api/`: Interaction with Gemma3.

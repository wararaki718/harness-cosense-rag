# DESIGN.md

Overall design documentation for the `harness-cosense-rag` project.

## RAG Flow Detail

### 1. Data Ingestion (Indexing Phase)
- **batch**: Periodically fetches content from target Cosense projects.
- **splade-api**: Encodes the fetched text into sparse vector representations.
- **batch** (orchestration): Receives the vectors from **splade-api** and indexes them into **elasticsearch**.
- **elasticsearch**: Stores the documents and sparse vectors for retrieval.

### 2. Retrieval & Generation (Query Phase)
- **UI**: Captures the user's natural language query and sends it to `search-api`.
- **search-api**: Orchestrates the search process.
    - Sends the query text to **splade-api** for vectorization.
    - Receives the returned **query vector** from **splade-api**.
    - Executes a search in **elasticsearch** using the query vector.
    - Retrieves the most relevant context snippets from the search results.
- **llm-api**: Sends the retrieved context and the user's query to **Ollama Gemma3**.
- **Response**: The generated answer is streamed back to the user via the UI.

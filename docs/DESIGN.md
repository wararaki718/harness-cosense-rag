# DESIGN.md

Overall design documentation for the `harness-cosense-rag` project.

## RAG Flow Detail

### 1. Data Ingestion (Indexing Phase)
- **batch**: Periodically fetches content from target Cosense projects.
- **splade-api**: Processes the fetched text using a SPLADE model to generate sparse vector representations.
- **elasticsearch**: Indexes the documents along with their sparse vectors for efficient retrieval.

### 2. Retrieval & Generation (Query Phase)
- **UI**: Captures the user's natural language query.
- **search-api**: Orchestrates the search process.
    - Sends the query to **splade-api** for vectorization.
    - Performs a vector search in **elasticsearch**.
    - Retrieves the most relevant context snippets.
- **llm-api**: Sends the retrieved context and the user's query to **Ollama Gemma3**.
- **Response**: The generated answer is streamed back to the user via the UI.

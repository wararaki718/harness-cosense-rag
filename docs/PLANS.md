# PLANS.md

High-level project plans and milestones for `harness-cosense-rag`.

## Implementation Roadmap

### Phase 1: Infrastructure & Core Services
- Set up **elasticsearch** instance.
- Develop **splade-api** for text encoding.
- Implement **batch** service for data ingestion from Cosense.

### Phase 2: Search & Generation
- Develop **search-api** to coordinate between SPLADE, Elasticsearch, and LLM.
- Integrate **llm-api** with **Ollama Gemma3**.

### Phase 3: Frontend & UX
- Build the **ui** for user interaction.
- Implement real-time answer streaming and source citations.

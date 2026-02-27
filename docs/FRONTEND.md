# FRONTEND.md

Frontend related documentation and design for `harness-cosense-rag`.

## UI Overview
The UI provides a simple interface for users to ask questions against the Cosense project data.

## Search Query Flow
1.  **Input**: User enters a natural language query in the search bar.
2.  **Request**: The UI sends the query to the `search-api`.
3.  **Processing**: The `search-api` orchestrates the flow: it vectorizes the query via `splade-api`, searches in `elasticsearch`, and then generates an answer using the LLM.
4.  **Display**: The generated answer is displayed in real-time (optionally via streaming) to the user, along with citations or links to the source Cosense pages.

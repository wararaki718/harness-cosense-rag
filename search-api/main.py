from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from elasticsearch import Elasticsearch
import requests
import os
from typing import List, Dict, Any

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
ES_HOST = os.getenv("ES_HOST", "http://elasticsearch:9200")
SPLADE_API_URL = os.getenv("SPLADE_API_URL", "http://splade-api:8001/encode")
LLM_API_URL = os.getenv("LLM_API_URL", "http://llm-api:8002/generate")
INDEX_NAME = "cosense-rag"

# Initialize ES client
es = Elasticsearch(ES_HOST)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    query: str
    answer: str
    context: List[Dict[str, Any]]

@app.get("/")
def read_root():
    return {"message": "search-api is running"}

@app.post("/search", response_model=SearchResult)
def search(request: SearchRequest):
    # 1. Encode query
    try:
        encode_resp = requests.post(SPLADE_API_URL, json={"text": request.query})
        encode_resp.raise_for_status()
        query_vector = encode_resp.json()["vector"]
    except Exception as e:
        print(f"Encoding failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to encode query")

    # 2. Search Elasticsearch
    # We use multiple 'rank_feature' queries wrapped in a 'should' (OR) bool query
    # to find documents that match the sparse vector tokens.
    should_clauses = []
    for token, weight in query_vector.items():
        should_clauses.append({
            "rank_feature": {
                "field": f"vector.{token}",
                "boost": weight
            }
        })

    search_body = {
        "query": {
            "bool": {
                "should": should_clauses
            }
        },
        "size": request.top_k
    }

    try:
        es_resp = es.search(index=INDEX_NAME, body=search_body)
        hits = es_resp["hits"]["hits"]
        
        contexts = []
        context_texts = []
        for hit in hits:
            source = hit["_source"]
            contexts.append({
                "title": source["title"],
                "url": source["url"],
                "score": hit["_score"]
            })
            context_texts.append(source["content"])
            
    except Exception as e:
        print(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to search Elasticsearch")

    # 3. Generate answer via llm-api
    try:
        llm_resp = requests.post(
            LLM_API_URL, 
            json={
                "query": request.query,
                "context": context_texts
            }
        )
        llm_resp.raise_for_status()
        answer = llm_resp.json()["answer"]
    except Exception as e:
        print(f"LLM generation failed: {e}")
        # Return results even if LLM fails
        answer = "Answer generation failed."

    return SearchResult(
        query=request.query,
        answer=answer,
        context=contexts
    )

import os
import time
import requests
from elasticsearch import Elasticsearch
from typing import List, Dict

# Configuration
COSENSE_PROJECT = os.getenv("COSENSE_PROJECT", "help") # Default to 'help' project
SPLADE_API_URL = os.getenv("SPLADE_API_URL", "http://splade-api:8001/encode")
ES_HOST = os.getenv("ES_HOST", "http://elasticsearch:9200")
INDEX_NAME = "cosense-rag"

def get_es_client():
    for _ in range(10):
        try:
            # Use requests for ping as Elasticsearch client might have issues with hostname resolution in some environments
            resp = requests.get(ES_HOST)
            if resp.status_code == 200:
                return Elasticsearch(ES_HOST)
        except Exception as e:
            print(f"Ping failed: {e}")
            pass
        print("Waiting for Elasticsearch...")
        time.sleep(5)
    raise Exception("Could not connect to Elasticsearch")

def create_index(es):
    """Create Elasticsearch index with sparse vector support if it doesn't exist."""
    print(f"Checking if index '{INDEX_NAME}' exists...")
    exists = False
    try:
        exists = es.indices.exists(index=INDEX_NAME)
    except Exception as e:
        print(f"Index existence check error (probably doesn't exist): {e}")
        exists = False

    if not exists:
        print(f"Creating index: {INDEX_NAME}")
        # SPLADE vectors are stored as 'rank_features' or 'flattened' with token weights
        mappings = {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "url": {"type": "keyword"},
                "vector": {"type": "rank_features"}
            }
        }
        es.indices.create(index=INDEX_NAME, mappings=mappings)

def fetch_cosense_pages(project: str) -> List[Dict]:
    """Fetch all pages from a Cosense project."""
    print(f"Fetching pages from Cosense project: {project}")
    url = f"https://scrapbox.io/api/pages/{project}?limit=100"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["pages"]

def fetch_page_content(project: str, title: str) -> str:
    """Fetch full content of a specific page."""
    url = f"https://scrapbox.io/api/pages/{project}/{title}/text"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_vector(text: str) -> Dict[str, float]:
    """Get sparse vector from splade-api."""
    try:
        response = requests.post(SPLADE_API_URL, json={"text": text})
        response.raise_for_status()
        return response.json()["vector"]
    except Exception as e:
        print(f"Error getting vector: {e}")
        return {}

def index_pages():
    """Main ingestion loop."""
    es = get_es_client()
    create_index(es)
    try:
        pages = fetch_cosense_pages(COSENSE_PROJECT)
        for page in pages:
            title = page["title"]
            print(f"Processing page: {title}")
            
            content = fetch_page_content(COSENSE_PROJECT, title)
            vector = get_vector(content)
            
            doc = {
                "title": title,
                "content": content,
                "url": f"https://scrapbox.io/{COSENSE_PROJECT}/{title}",
                "vector": vector
            }
            
            es.index(index=INDEX_NAME, id=page["id"], document=doc)
            print(f"Indexed: {title}")
            
    except Exception as e:
        print(f"Ingestion failed: {e}")

if __name__ == "__main__":
    import sys
    if "--sync" in sys.argv:
        index_pages()
    else:
        print("Batch service is idle. Run with --sync to start ingestion.")
        while True:
            time.sleep(60)

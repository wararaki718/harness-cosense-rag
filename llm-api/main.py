from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from typing import List

app = FastAPI()

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:latest")

class GenerateRequest(BaseModel):
    query: str
    context: List[str]

class GenerateResponse(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return {"message": "llm-api is running", "ollama_url": OLLAMA_BASE_URL, "model": MODEL_NAME}

@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    context_str = "\n\n".join(request.context)
    prompt = f"""
以下のコンテキスト（検索結果）を参考にして、ユーザーの質問に日本語で答えてください。
コンテキスト内に答えがない場合は「提供された情報には答えが見つかりませんでした」と答えてください。

コンテキスト:
{context_str}

質問:
{request.query}

回答:
"""
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        result = response.json()
        return GenerateResponse(answer=result["response"])
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        raise HTTPException(status_code=500, detail=str(e))

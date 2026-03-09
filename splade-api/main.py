from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForMaskedLM, AutoTokenizer
import torch
import numpy as np
from typing import Dict, List

app = FastAPI()

# Model configuration
MODEL_ID = "naver/splade_v2_distil"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Global variables for model and tokenizer
model = None
tokenizer = None

@app.on_event("startup")
def load_model():
    global model, tokenizer
    print(f"Loading SPLADE model: {MODEL_ID} on {device}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForMaskedLM.from_pretrained(MODEL_ID)
    model.to(device)
    model.eval()
    print("Model loaded successfully.")

class EncodeRequest(BaseModel):
    text: str

class EncodeResponse(BaseModel):
    vector: Dict[str, float]

@app.get("/")
def read_root():
    return {"message": "splade-api is running", "model": MODEL_ID, "device": str(device)}

@app.get("/health")
def health():
    if model is not None and tokenizer is not None:
        return {"status": "ready"}
    return {"status": "loading"}

@app.post("/encode", response_model=EncodeResponse)
def encode(request: EncodeRequest):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    with torch.no_grad():
        inputs = tokenizer(request.text, return_tensors="pt").to(device)
        outputs = model(**inputs)
        logits = outputs.logits
        
        # SPLADE encoding logic: log(1 + relu(logits)) * attention_mask
        # We take the maximum over the sequence dimension (dim=1)
        weights = torch.log1p(torch.relu(logits))
        
        # Apply attention mask to ignore padding tokens
        # sparse_vector shape: [vocab_size]
        sparse_vector = torch.max(weights * inputs['attention_mask'].unsqueeze(-1), dim=1).values[0]
        
        # Filter non-zero weights
        indices = torch.nonzero(sparse_vector).squeeze().cpu().tolist()
        if isinstance(indices, int): # Handle case with single non-zero element
            indices = [indices]
            
        result = {}
        for idx in indices:
            token = tokenizer.decode([idx]).strip()
            if token and token not in ["[CLS]", "[SEP]", "[PAD]"]:
                # Elasticsearch rank_features do not support dots in feature names
                safe_token = token.replace(".", "_")
                result[safe_token] = float(sparse_vector[idx].item())
        
        return EncodeResponse(vector=result)

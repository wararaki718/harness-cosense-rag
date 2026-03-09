from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "splade-api is running"}

@app.post("/encode")
def encode(text: str):
    return {"vector": [0.1, 0.2, 0.3]} # Placeholder

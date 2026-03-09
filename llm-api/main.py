from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "llm-api is running"}

@app.post("/generate")
def generate(prompt: str):
    return {"response": "This is a placeholder response for: " + prompt}

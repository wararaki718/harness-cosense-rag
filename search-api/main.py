from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "search-api is running"}

@app.get("/search")
def search(query: str):
    return {"results": ["Result 1", "Result 2"]} # Placeholder

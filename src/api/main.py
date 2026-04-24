from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/query")
def query(req: QueryRequest):
    # Placeholder response for production scaffold
    return {
        "question": req.question,
        "generated_sql": "SELECT 'demo' as result",
        "result": [{"result": "demo"}]
    }

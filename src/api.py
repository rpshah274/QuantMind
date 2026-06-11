from fastapi import FastAPI
from pydantic import BaseModel
from src.generator import generate_answer
from src.metrics import get_metrics, format_metrics
from src.news import fetch_news

app = FastAPI(title="QuantMind API")

class AnalyzeRequest(BaseModel):
    question: str

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    # call generate_answer and return result
    result = ""
    for chunk in generate_answer(request.question):
        result += chunk
    return {"answer": result}

@app.get("/metrics/{ticker}")
def metrics(ticker: str):
    # call get_metrics and return result
    return get_metrics(ticker.upper())

@app.get("/news/{ticker}")
def news(ticker: str, company_name: str):
    # call fetch_news and return result
    return fetch_news(ticker,company_name)
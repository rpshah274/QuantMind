from groq import Groq
from dotenv import load_dotenv
import os
from src.retriever import query_collection, index_chunks
from src.metrics import get_metrics, format_metrics
from src.news import index_news, fetch_news
from src.edgar import download_10k
import asyncio
from concurrent.futures import ThreadPoolExecutor
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# Extract Ticker info from query
def extract_ticker(question: str) -> tuple[str, str]:
    """
    Use Groq to extract ticker and company name from question.
    Returns (ticker, company_name) e.g. ("AAPL", "Apple Inc.")
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Extract the stock ticker symbol and company name from the question. Reply with ONLY two words separated by a comma: TICKER,Company Name. Example: AAPL,Apple Inc."},
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    result = response.choices[0].message.content.strip()
    ticker, company_name = result.split(",", 1)
    return ticker.strip().upper(), company_name.strip()
# Threading
def _prepare_filing(ticker: str) -> None:
    import os
    filing_path = f"data/filings/{ticker}_10k.txt"
    if not os.path.exists(filing_path):
        path = download_10k(ticker)
        chunks = chunk_filing(ticker, path)
    else:
        from src.chunker import chunk_filing
        chunks = chunk_filing(ticker, filing_path)
    index_chunks(chunks, ticker)

def prepare_all(ticker: str, company_name: str) -> dict:
    with ThreadPoolExecutor(max_workers=3) as executor:
        filing_future = executor.submit(_prepare_filing, ticker)
        news_future = executor.submit(index_news, ticker, company_name)
        metrics_future = executor.submit(get_metrics, ticker)
        
        filing_future.result()
        news_future.result()
        metrics = metrics_future.result()
    return metrics

def generate_answer(question: str):
    # Extract ticker and company details
    ticker, company_name = extract_ticker(question)
    print(f"Detected: {ticker} — {company_name}")
    # Prepare all data sources parallely
    metrics = prepare_all(ticker, company_name)
    metrics_text = format_metrics(metrics)
    # Retrieve relevant chunks & news
    filing_chunks = query_collection(question, ticker, n_results=5)
    filing_context = "\n\n".join(filing_chunks)
    news_chunks = query_collection(question, f"{ticker}_news", n_results=3)
    news_context = "\n\n".join(news_chunks)
    # Build prompt string combining all 3 
    prompt = f"""
    FINANCIAL METRICS:
    {metrics_text}

    RELEVANT 10-K EXCERPTS:
    {filing_context}

    RECENT NEWS:
    {news_context}

    QUESTION: {question}

    Provide a structured financial analysis with clear sections. Cite specific numbers from the metrics and filings.
    """
    
    response = client.chat.completions.create(
           model="llama-3.3-70b-versatile",
           messages=[
               {"role": "system", "content": "You are an expert financial analyst. Analyze companies based on SEC filings, financial metrics, and recent news. Always cite specific numbers and be objective."},
               {"role": "user", "content": prompt}],
           temperature=0.1,
           stream=True)
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
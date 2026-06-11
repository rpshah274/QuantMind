import requests
from dotenv import load_dotenv
import os
from src.chunker import chunk_text
from src.retriever import get_or_create_collection, chroma_client
from src.embedder import embed_text
import time

load_dotenv()
NEWS_API_KEY = os.getenv("NEWSAPI_KEY")

def fetch_news(ticker: str, company_name: str, days_back: int = 7) -> list[dict]:
    # Call NewsAPI everything endpoint
    response = requests.get("https://newsapi.org/v2/everything",
                params=
                {
                "q": f"{ticker} {company_name}",
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 20,
                "apiKey": NEWS_API_KEY
                })
    articles = response.json()["articles"]
    res=[]
    for i,article in enumerate(articles):
        # skip articles where title or description is None
        if article["title"] is None or article["description"] is None:
            continue
        res.append(
            {
            "ticker": ticker,
            "chunk_id": f"{ticker}_news_{i}",
            "text": f"{article['title']}. {article['description']}",
            "source": "news",
            "url": article["url"],
            "published_at": article["publishedAt"]
            }
        )
    return res

def index_news(ticker: str, company_name: str) -> None:
    """
    1. Fetch news using fetch_news()
    2. Get or create collection named f"{ticker}_news"
    3. Embed each article text using embed_text()
    4. Add to collection using collection.add()
    5. Print how many articles indexed
    
    Add time.sleep(0.7) between embeddings — same rate limit reason
    """
    # Fetch news
    news = fetch_news(ticker,company_name)
    collection = get_or_create_collection(f"{ticker}_news")

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    # Get or create collection and Embed each article
    for article in news:
        embedding = embed_text(article["text"])
        # append to ids, embeddings, documents, metadatas
        ids.append(article["chunk_id"])
        embeddings.append(embedding)
        documents.append(article["text"])
        metadatas.append({"ticker":ticker,"source":"news","url":article["url"]})
        time.sleep(0.7)
    collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    print(f"Indexed {len(news)} articles for {ticker}")
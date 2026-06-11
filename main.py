from src.edgar import get_cik, get_latest_10k_url, download_10k

# # Test 1
# cik = get_cik("AAPL")
# print(f"CIK: {cik}")

# # Test 2
# url = get_latest_10k_url(cik)
# print(f"URL: {url}")

# # Test 3
# path = download_10k("AAPL")
# print(f"Saved to: {path}")
# print(f"CIK: {cik}")
# path = download_10k("AAPL")
# print(f"Downloaded to: {path}")

# from src.chunker import chunk_filing

# path = download_10k("AAPL")
# chunks = chunk_filing("AAPL", path)

# print(f"Total chunks: {len(chunks)}")
# print(f"\nFirst chunk preview:")
# print(chunks[0]["text"][:300])

# from src.embedder import embed_text

# vec = embed_text("Apple revenue declined")
# print(f"Vector length: {len(vec)}")
# print(f"First 5 values: {vec[:5]}")

# from src.retriever import index_chunks, query_collection

# # Download and chunk
# path = download_10k("AAPL")
# chunks = chunk_filing("AAPL", path)
# print(f"Total chunks: {len(chunks)}")

# # Embed and index (takes ~2 minutes)
# index_chunks(chunks, "AAPL")

# # Query
# question = "What are Apple's key liquidity risks?"
# results = query_collection(question, "AAPL")

# print(f"\nQuestion: {question}")
# print(f"\nTop 5 relevant chunks:")
# for i, chunk in enumerate(results):
#     print(f"\n--- Chunk {i+1} ---")
#     print(chunk[:300])

# from src.news import fetch_news

# articles = fetch_news("AAPL", "Apple")
# print(f"Total articles: {len(articles)}")
# print(f"\nFirst article:")
# print(articles[0])

# from src.news import index_news, fetch_news
# from src.retriever import query_collection

# # Index news
# index_news("AAPL", "Apple")

# # Query news collection
# results = query_collection("Apple WWDC announcements", "AAPL_news")
# for i, chunk in enumerate(results):
#     print(f"\n--- Article {i+1} ---")
#     print(chunk[:300])

# from src.metrics import get_metrics
# metrics = get_metrics("AAPL")
# print(metrics)

from src.metrics import get_metrics, format_metrics
print(format_metrics(get_metrics("AAPL")))

from src.generator import generate_answer

answer = generate_answer(
    "Give me a fundamental analysis of Apple",
    "AAPL",
    "Apple"
)
print(answer)
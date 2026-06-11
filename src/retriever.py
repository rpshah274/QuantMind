import chromadb
from src.embedder import embed_text, embed_chunks

# ChromaDB client — stores data locally in ./chroma_db folder
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def get_or_create_collection(ticker: str):
    # ChromaDB organizes data into collections, one collection per ticker.
    return chroma_client.get_or_create_collection(ticker)

def index_chunks(chunks: list[dict], ticker: str) -> None:
    collection = get_or_create_collection(ticker)
    embedded_chunks = embed_chunks(chunks)
    collection.add(
        ids=[chunk["chunk_id"] for chunk in embedded_chunks],
        embeddings=[chunk["embedding"] for chunk in embedded_chunks],
        documents=[chunk["text"] for chunk in embedded_chunks],
        metadatas=[{"ticker": chunk["ticker"], "source": chunk["source"]} for chunk in embedded_chunks]
    )
    print(f"Indexed {len(embedded_chunks)} chunks for {ticker}")

def query_collection(question: str, ticker: str, n_results: int = 5) -> list[str]:
    collection = get_or_create_collection(ticker)
    question_vector = embed_text(question, task_type="RETRIEVAL_QUERY")
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=n_results)
    return results["documents"][0]
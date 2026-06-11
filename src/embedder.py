from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str, task_type: str="RETRIEVAL_DOCUMENT") -> list[float]:
    return model.encode(text).tolist()

def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    For each chunk in chunks:
    1. Call embed_text on chunk["text"]
    2. Add the result as chunk["embedding"]
    3. Return the updated list
    
    Note: print progress every 50 chunks so you
    know it's working (276 chunks takes ~30 seconds)
    """
    res=[]
    for i,chunk in enumerate(chunks):
        chunk["embedding"] = embed_text(chunk["text"])
        if i % 50 == 0:
            print(f"Embedded {i}/{len(chunks)} chunks")
        res.append(chunk)
        # time.sleep(0.7)
    return res
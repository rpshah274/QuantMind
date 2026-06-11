from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

def load_text(file_path: str) -> str:
    # Read the file and return it
    with open(file_path,"r",encoding="utf-8") as f:
        return f.read()

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

def chunk_filing(ticker: str, file_path: str) -> list[dict]:
    # Load the text
    text = load_text(file_path)
    # Chunk it
    chunks = chunk_text(text)
    res=[]
    for i,chunk in enumerate(chunks):
        res.append({
                "ticker": ticker,
                "chunk_id": f"{ticker}_chunk_{i}",
                "text": chunk,
                "source": "10-K"
        })
    return res
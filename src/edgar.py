import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup
# SEC requires header on every request
HEADERS = {"User-Agent": "QuantMind rushi.shah2704@email.com"}

def get_cik(ticker: str) -> str:
    response=requests.get("https://www.sec.gov/files/company_tickers.json",headers=HEADERS)
    data = response.json()
    # Loop through the values and find entry where ticker matches
    for company in data.values():
        if company["ticker"].upper() == ticker.upper():
            cik=company["cik_str"]
            # Return cik as zero-padded 10-digit string
            return  str(cik).zfill(10)      
      
def get_latest_10k_url(cik: str) -> str:
    response = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json",headers=HEADERS)
    data = response.json()
    # Get the "recent" filings dict
    recent = data["filings"]["recent"] 
    # Find the index of "10-K" in the forms list
    index = recent["form"].index("10-K")
    # Get accessionNumber and primaryDocument at that index
    accession = recent["accessionNumber"][index]
    primary = recent["primaryDocument"][index]
    # Remove dashes from accessionNumber
    accession_clean = accession.replace("-","")
    # build the URL
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_clean}/{primary}"    
    print(f"accession raw: {accession}")
    print(f"accession clean: {accession_clean}")
    print(f"primary: {primary}")
    print(f"cik: {cik}")
    print(f"url: {url}")
    return url

def download_10k(ticker: str, save_dir: str = "data/filings") -> str:
    cik = get_cik(ticker)
    url = get_latest_10k_url(cik)
    # Fetch the document
    response = requests.get(url,headers=HEADERS)
    data = response.text
    # Create save_dir if it doesn't exist
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    file_path = f"{save_dir}/{ticker}_10k.txt"
    # Save as {save_dir}/{ticker}_10k.txt
    # Save raw HTML first
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
    # clean it
    clean_text = clean_html(file_path)
    # overwrite with clean text
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(clean_text)
    return file_path

def clean_html(file_path: str) -> str:
    # Read the file and clean it using BeautifulSoup
    with open(file_path, "r", encoding="utf-8") as f:
        clean = BeautifulSoup(f,"html.parser")
        return clean.get_text(" ",strip=True)
import json
import os
import requests

from pypdf import PdfReader

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk


nltk.download('stopwords')
nltk.download('punkt')


# 1) TOKENIZATION 


def compressedTokenize(text):
    stemmer = PorterStemmer()
    stopWords = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    filtered = [t for t in tokens if t.isalpha() and t not in stopWords]
    return [stemmer.stem(t) for t in filtered]



# 2) PARSE SPECTRUM DOCS


pdfDir = "pdfs"
thesisJson = "spectrum_pdfs_1000.json"   


def download_pdf(url):
    """
    Download a PDF from Spectrum and save it under PDF_DIR.
    Returns the local file path.
    """
    os.makedirs(pdfDir, exist_ok=True)
    filename = url.split("/")[-1] or "document.pdf"
    localPath = os.path.join(pdfDir, filename)

    if os.path.exists(localPath):
        # Already downloaded
        return localPath

    print(f"[DL] {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    with open(localPath, "wb") as f:
        f.write(resp.content)

    return localPath


def extractPdf(pdf_path):
    
    textChunks = []
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            textChunks.append(page_text)
    return "\n".join(textChunks)


def parseSpectrum():
    """
    Similar idea to parseReuters():
    Returns a list of dicts with:
      - docId
      - title
      - body
    """
    with open(thesisJson, "r", encoding="utf-8") as f:
        items = json.load(f)

    documents = []

    for i, item in enumerate(items):
        pdf_url = item["pdf_url"]
        record_url = item.get("thesis_record", "")
        thesis_type = item.get("thesis_type", "")

        try:
            pdf_path = download_pdf(pdf_url)
            body_text = extractPdf(pdf_path)
        except Exception as e:
            print(f"[ERROR] Skipping {pdf_url} because: {e}")
            continue

        # Use record URL or thesis type as a "title" placeholder
        title = f"{thesis_type.upper()} - {record_url}"

        documents.append({
            "docId": i,        # just use index i as docId (like Reuters)
            "title": title,
            "body": body_text
        })

        print(f"[OK] Parsed docId={i} from {pdf_url}")

    return documents



# 3) BUILD INDEX 


def buildIndex():
    documents = parseSpectrum()
    index = {}

    for doc in documents:
        docId = doc["docId"]
        text = (doc["title"] + " " + doc["body"]).strip()
        tokens = compressedTokenize(text)

        for token in tokens:
            if token not in index:
                index[token] = [docId]
            elif docId not in index[token]:
                index[token].append(docId)

    # Save index if you want
    with open("spectrum_index.json", "w", encoding="utf-8") as f:
        json.dump(index, f)

    print(f"\nBuilt index with {len(index)} terms over {len(documents)} documents.")
    return index


if __name__ == "__main__":
    buildIndex()

import io
import pdfplumber
from docx import Document
from bs4 import BeautifulSoup

def parse_document(content: bytes, url: str) -> str:
    if url.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif url.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs if p.text)
    elif url.endswith(".html"):
        soup = BeautifulSoup(content, "html.parser")
        return soup.get_text()
    else:
        return content.decode("utf-8")

import io
from docx import Document
from bs4 import BeautifulSoup
import fitz  # PyMuPDF: pip install pymupdf

def parse_document(content: bytes, url: str) -> str:
    if url.endswith(".pdf"):
        try:
            all_text = []
            pdf = fitz.open(stream=content, filetype="pdf")
            for i, page in enumerate(pdf):
                text = page.get_text()
                if text:
                    all_text.append(text)
            return "\n".join(all_text)
        except Exception as e:
            print(f"[ERROR] PDF parsing failed: {e}")
            return ""
    elif url.endswith(".docx"):
        try:
            doc = Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs if p.text)
        except Exception as e:
            print(f"[ERROR] DOCX parsing failed: {e}")
            return ""
    elif url.endswith(".html"):
        try:
            soup = BeautifulSoup(content, "html.parser")
            return soup.get_text()
        except Exception as e:
            print(f"[ERROR] HTML parsing failed: {e}")
            return ""
    else:
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return ""  # 디코딩 실패 시 빈 문자열 반환

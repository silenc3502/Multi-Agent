import io
from docx import Document as DocxDocument
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from documents_analysis.domain.entity.DocumentType import DocumentType


class DocumentParser:
    @staticmethod
    def parse(content: bytes, doc_type: DocumentType) -> str:
        if doc_type == DocumentType.PDF:
            pdf = fitz.open(stream=content, filetype="pdf")
            return "\n".join(page.get_text() for page in pdf)

        elif doc_type == DocumentType.DOCX:
            doc = DocxDocument(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs if p.text)

        elif doc_type in [DocumentType.HTML, DocumentType.XML]:
            soup = BeautifulSoup(content, "html.parser")
            return soup.get_text()

        elif doc_type == DocumentType.TEXT:
            return content.decode("utf-8", errors="ignore")

        else:
            raise ValueError(f"지원하지 않는 문서 타입: {doc_type}")
